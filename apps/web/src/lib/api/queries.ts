"use client";

import type {
  Account,
  AccountInput,
  Category,
  CategoryInput,
  Me,
  Schemas,
  Transaction,
  TransactionPage,
} from "@budget/api-client";
import { useMutation, useMutationState, useQuery, useQueryClient } from "@tanstack/react-query";
import { endOfMonth, startOfMonth } from "date-fns";
import { toast } from "sonner";
import { monthKey, toISODate } from "@/lib/format";
import { api, call, setActiveHousehold } from "./client";
import { errorMessage } from "./errors";
import { mk, qk } from "./keys";
import type { DeleteTransactionVars, PutTransactionVars } from "./query-client";

// --- reads -----------------------------------------------------------------------------------

export function useMe() {
  return useQuery({
    queryKey: qk.me,
    queryFn: async () => {
      const me = await call<Me>(api.GET("/v1/me"));
      setActiveHousehold(me.household.id);
      return me;
    },
    staleTime: 5 * 60_000,
  });
}

export function useAccounts() {
  return useQuery({
    queryKey: qk.accounts,
    queryFn: () => call<Account[]>(api.GET("/v1/accounts")),
  });
}

export function useCategories() {
  return useQuery({
    queryKey: qk.categories,
    queryFn: () => call<Category[]>(api.GET("/v1/categories")),
    staleTime: 5 * 60_000,
  });
}

async function fetchMonth(month: Date): Promise<Transaction[]> {
  const items: Transaction[] = [];
  let cursor: string | undefined;
  do {
    const page: TransactionPage = await call(
      api.GET("/v1/transactions", {
        params: {
          query: {
            from: toISODate(startOfMonth(month)),
            to: toISODate(endOfMonth(month)),
            limit: 500,
            cursor,
          },
        },
      }),
    );
    items.push(...page.items);
    cursor = page.next_cursor ?? undefined;
  } while (cursor);
  return items;
}

export function useMonthTransactions(month: Date) {
  return useQuery({
    queryKey: qk.month(monthKey(month)),
    queryFn: () => fetchMonth(month),
  });
}

/** Ids of transactions still waiting to reach the server (offline or in flight). */
export function usePendingTransactionIds() {
  const ids = useMutationState({
    filters: { mutationKey: mk.putTransaction, status: "pending" },
    select: (m) => (m.state.variables as PutTransactionVars | undefined)?.id,
  });
  return new Set(ids.filter(Boolean) as string[]);
}

// --- transaction writes (optimistic, offline-capable) ----------------------------------------

function sortTransactions(list: Transaction[]) {
  return list.sort(
    (a, b) => b.date.localeCompare(a.date) || b.created_at.localeCompare(a.created_at),
  );
}

export function useSaveTransaction() {
  const qc = useQueryClient();
  return useMutation<
    unknown,
    Error,
    PutTransactionVars,
    { snapshot: [readonly unknown[], unknown][] }
  >({
    mutationKey: mk.putTransaction,
    onMutate: async ({ id, body }) => {
      await qc.cancelQueries({ queryKey: qk.transactions });
      const snapshot = qc.getQueriesData({ queryKey: ["transactions", "month"] });
      const now = new Date().toISOString();
      let previous: Transaction | undefined;
      for (const [key, data] of snapshot) {
        const list = data as Transaction[] | undefined;
        previous ??= list?.find((t) => t.id === id);
        if (list)
          qc.setQueryData(
            key,
            list.filter((t) => t.id !== id),
          );
      }
      const optimistic: Transaction = {
        installment_group_id: null,
        installment_number: null,
        installment_total: null,
        recurring_rule_id: null,
        invoice_month: null,
        created_at: now,
        ...previous,
        ...body,
        to_account_id: body.to_account_id ?? null,
        category_id: body.category_id ?? null,
        member_id: body.member_id ?? null,
        notes: body.notes ?? null,
        paid: body.paid ?? true,
        id,
        updated_at: now,
      };
      qc.setQueryData<Transaction[]>(qk.month(body.date.slice(0, 7)), (list) =>
        list ? sortTransactions([optimistic, ...list]) : list,
      );
      return { snapshot };
    },
    onError: (error, _vars, context) => {
      for (const [key, data] of context?.snapshot ?? []) qc.setQueryData(key, data);
      toast.error(errorMessage(error));
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: qk.transactions });
      qc.invalidateQueries({ queryKey: qk.accounts });
    },
  });
}

export function useDeleteTransaction() {
  const qc = useQueryClient();
  return useMutation<
    unknown,
    Error,
    DeleteTransactionVars,
    { snapshot: [readonly unknown[], unknown][] }
  >({
    mutationKey: mk.deleteTransaction,
    onMutate: async ({ id }) => {
      await qc.cancelQueries({ queryKey: qk.transactions });
      const snapshot = qc.getQueriesData({ queryKey: ["transactions", "month"] });
      for (const [key, data] of snapshot) {
        const list = data as Transaction[] | undefined;
        if (list)
          qc.setQueryData(
            key,
            list.filter((t) => t.id !== id),
          );
      }
      return { snapshot };
    },
    onError: (error, _vars, context) => {
      for (const [key, data] of context?.snapshot ?? []) qc.setQueryData(key, data);
      toast.error(errorMessage(error));
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: qk.transactions });
      qc.invalidateQueries({ queryKey: qk.accounts });
    },
  });
}

// --- accounts / categories / profile ---------------------------------------------------------

type AccountUpdate = Schemas["AccountUpdate"];
type CategoryUpdate = Schemas["CategoryUpdate"];
type MeUpdate = Schemas["MeUpdate"];

function useInvalidatingMutation<V>(
  fn: (vars: V) => Promise<unknown>,
  keys: readonly (readonly string[])[],
) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: fn,
    onError: (error) => toast.error(errorMessage(error)),
    onSettled: () => Promise.all(keys.map((queryKey) => qc.invalidateQueries({ queryKey }))),
  });
}

export const useCreateAccount = () =>
  useInvalidatingMutation(
    (body: AccountInput) => call<Account>(api.POST("/v1/accounts", { body })),
    [qk.accounts],
  );

export const useUpdateAccount = () =>
  useInvalidatingMutation(
    ({ id, body }: { id: string; body: AccountUpdate }) =>
      call<Account>(
        api.PATCH("/v1/accounts/{account_id}", { params: { path: { account_id: id } }, body }),
      ),
    [qk.accounts],
  );

export const useDeleteAccount = () =>
  useInvalidatingMutation(
    (id: string) =>
      call(api.DELETE("/v1/accounts/{account_id}", { params: { path: { account_id: id } } })),
    [qk.accounts],
  );

export const useCreateCategory = () =>
  useInvalidatingMutation(
    (body: CategoryInput) => call<Category>(api.POST("/v1/categories", { body })),
    [qk.categories],
  );

export const useUpdateCategory = () =>
  useInvalidatingMutation(
    ({ id, body }: { id: string; body: CategoryUpdate }) =>
      call<Category>(
        api.PATCH("/v1/categories/{category_id}", { params: { path: { category_id: id } }, body }),
      ),
    [qk.categories],
  );

export const useDeleteCategory = () =>
  useInvalidatingMutation(
    (id: string) =>
      call(api.DELETE("/v1/categories/{category_id}", { params: { path: { category_id: id } } })),
    [qk.categories],
  );

export function useUpdateMe() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: MeUpdate) => call<Me>(api.PATCH("/v1/me", { body })),
    onSuccess: (me) => qc.setQueryData(qk.me, me),
    onError: (error) => toast.error(errorMessage(error)),
  });
}
