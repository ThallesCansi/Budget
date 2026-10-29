import type { TransactionInput } from "@budget/api-client";
import { QueryClient } from "@tanstack/react-query";
import { api, call } from "./client";
import { ApiError } from "./errors";
import { mk } from "./keys";

export type PutTransactionVars = { id: string; body: TransactionInput };
export type DeleteTransactionVars = { id: string };

const WEEK = 1000 * 60 * 60 * 24 * 7;

export function makeQueryClient() {
  const client = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        gcTime: WEEK,
        retry: (count, error) => !(error instanceof ApiError && error.status < 500) && count < 2,
      },
      mutations: {
        // Validation errors won't succeed on retry; network failures will.
        retry: (count, error) => !(error instanceof ApiError) && count < 3,
      },
    },
  });

  // Defaults (not inline mutationFns) so mutations paused offline can resume after a reload.
  client.setMutationDefaults(mk.putTransaction, {
    mutationFn: ({ id, body }: PutTransactionVars) =>
      call(
        api.PUT("/v1/transactions/{transaction_id}", {
          params: { path: { transaction_id: id } },
          body,
        }),
      ),
  });
  client.setMutationDefaults(mk.deleteTransaction, {
    mutationFn: ({ id }: DeleteTransactionVars) =>
      call(
        api.DELETE("/v1/transactions/{transaction_id}", {
          params: { path: { transaction_id: id } },
        }),
      ),
  });
  return client;
}
