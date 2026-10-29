"use client";

import type { Transaction, TransactionKind } from "@budget/api-client";
import { Check, Search, SearchX, Trash2, Undo2 } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useMemo, useState } from "react";
import { EmptyState } from "@/components/empty-state";
import { Chip } from "@/components/forms/chip";
import { MonthSwitcher, MonthTransition } from "@/components/layout/month-switcher";
import { PageHeader } from "@/components/layout/page-header";
import { Money } from "@/components/money";
import { Shimmer } from "@/components/motion/skeleton";
import { SwipeRow } from "@/components/motion/swipe-row";
import { useMonth } from "@/components/providers/month-provider";
import { TransactionRow } from "@/components/transactions/transaction-row";
import { toInput, useTransactionSheet } from "@/components/transactions/transaction-sheet";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  useAccounts,
  useCategories,
  useMonthTransactions,
  usePendingTransactionIds,
  useSaveTransaction,
} from "@/lib/api/queries";
import { formatDayHeading } from "@/lib/format";
import { spring } from "@/lib/motion";
import { monthTotals } from "@/lib/summary";

const KIND_FILTERS: { value: TransactionKind | "all"; label: string }[] = [
  { value: "all", label: "Todas" },
  { value: "expense", label: "Despesas" },
  { value: "income", label: "Receitas" },
  { value: "transfer", label: "Transferências" },
];

const normalize = (s: string) =>
  s
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();

export function TransactionsView() {
  const { month } = useMonth();
  const { data: transactions, isPending } = useMonthTransactions(month);
  const { data: accounts = [] } = useAccounts();
  const { data: categories = [] } = useCategories();
  const pendingIds = usePendingTransactionIds();
  const sheet = useTransactionSheet();
  const save = useSaveTransaction();

  const [kind, setKind] = useState<TransactionKind | "all">("all");
  const [accountId, setAccountId] = useState("all");
  const [query, setQuery] = useState("");

  const accountById = useMemo(() => new Map(accounts.map((a) => [a.id, a] as const)), [accounts]);
  const categoryById = useMemo(
    () => new Map(categories.map((c) => [c.id, c] as const)),
    [categories],
  );

  const filtered = useMemo(() => {
    const q = normalize(query.trim());
    return (transactions ?? []).filter((t) => {
      if (kind !== "all" && t.kind !== kind) return false;
      if (accountId !== "all" && t.account_id !== accountId && t.to_account_id !== accountId)
        return false;
      if (!q) return true;
      const category = t.category_id ? categoryById.get(t.category_id)?.name : "";
      return normalize(`${t.description} ${category ?? ""} ${t.notes ?? ""}`).includes(q);
    });
  }, [transactions, kind, accountId, query, categoryById]);

  const groups = useMemo(() => {
    const map = new Map<string, Transaction[]>();
    for (const t of filtered) map.set(t.date, [...(map.get(t.date) ?? []), t]);
    return [...map.entries()];
  }, [filtered]);

  const totals = monthTotals(filtered);
  const togglePaid = (t: Transaction) =>
    save.mutate({ id: t.id, body: { ...toInput(t), paid: !t.paid } });

  return (
    <div className="space-y-5">
      <PageHeader title="Transações" />

      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div className="flex justify-center">
          <MonthSwitcher />
        </div>
        <div className="flex gap-2">
          <div className="relative flex-1 md:w-64">
            <Search className="text-muted-foreground pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2" />
            <Input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Buscar lançamentos"
              className="h-10 pl-9 text-base md:text-sm"
              aria-label="Buscar lançamentos"
            />
          </div>
          <Select value={accountId} onValueChange={setAccountId}>
            <SelectTrigger className="h-10 w-36" aria-label="Filtrar por conta">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas as contas</SelectItem>
              {accounts.map((a) => (
                <SelectItem key={a.id} value={a.id}>
                  {a.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="-mx-4 flex gap-2 overflow-x-auto px-4 md:mx-0 md:px-0">
        {KIND_FILTERS.map((f) => (
          <Chip key={f.value} selected={kind === f.value} onClick={() => setKind(f.value)}>
            {f.label}
          </Chip>
        ))}
      </div>

      <div className="bg-card shadow-card grid grid-cols-3 gap-2 rounded-2xl border p-3 text-center">
        <div>
          <p className="text-muted-foreground text-xs">Entradas</p>
          <Money cents={totals.income} tone="income" animate className="font-semibold" />
        </div>
        <div>
          <p className="text-muted-foreground text-xs">Saídas</p>
          <Money cents={totals.expense} tone="expense" animate className="font-semibold" />
        </div>
        <div>
          <p className="text-muted-foreground text-xs">Resultado</p>
          <Money cents={totals.net} tone="auto" animate className="font-semibold" />
        </div>
      </div>

      <p className="text-muted-foreground text-center text-xs md:hidden">
        Deslize para a direita para marcar como pago, ou para a esquerda para excluir.
      </p>

      <MonthTransition>
        {isPending && !transactions ? (
          <div className="space-y-2">
            {[0, 1, 2, 3, 4].map((i) => (
              <Shimmer key={i} className="h-16" />
            ))}
          </div>
        ) : groups.length === 0 ? (
          <EmptyState
            icon={SearchX}
            title={transactions?.length ? "Nada encontrado" : "Nenhum lançamento neste mês"}
            description={
              transactions?.length
                ? "Tente outra busca ou limpe os filtros."
                : "Toque no + para registrar uma despesa, receita ou transferência."
            }
          />
        ) : (
          <div className="space-y-6">
            {groups.map(([date, items]) => {
              const dayTotals = monthTotals(items);
              return (
                <section key={date} aria-label={formatDayHeading(date)}>
                  <div className="mb-2 flex items-baseline justify-between px-1">
                    <h2 className="text-muted-foreground text-sm font-semibold">
                      {formatDayHeading(date)}
                    </h2>
                    <Money cents={dayTotals.net} tone="muted" sign className="text-xs" />
                  </div>
                  <motion.ul layout className="space-y-2">
                    <AnimatePresence initial={false}>
                      {items.map((t) => (
                        <motion.li
                          key={t.id}
                          layout
                          initial={{ opacity: 0, y: -8, scale: 0.98 }}
                          animate={{ opacity: 1, y: 0, scale: 1 }}
                          exit={{ opacity: 0, x: -60, height: 0, marginTop: 0 }}
                          transition={spring.gentle}
                          className="shadow-card overflow-hidden rounded-xl border"
                        >
                          <SwipeRow
                            left={{
                              label: t.paid ? "Previsto" : "Pago",
                              icon: t.paid ? (
                                <Undo2 className="size-5" />
                              ) : (
                                <Check className="size-5" />
                              ),
                              className: "bg-income",
                              onTrigger: () => togglePaid(t),
                            }}
                            right={{
                              label: "Excluir",
                              icon: <Trash2 className="size-5" />,
                              className: "bg-expense",
                              onTrigger: () => sheet.remove(t),
                            }}
                          >
                            <TransactionRow
                              transaction={t}
                              category={t.category_id ? categoryById.get(t.category_id) : undefined}
                              account={accountById.get(t.account_id)}
                              toAccount={
                                t.to_account_id ? accountById.get(t.to_account_id) : undefined
                              }
                              pending={pendingIds.has(t.id)}
                              onClick={() => sheet.edit(t)}
                            />
                          </SwipeRow>
                        </motion.li>
                      ))}
                    </AnimatePresence>
                  </motion.ul>
                </section>
              );
            })}
          </div>
        )}
      </MonthTransition>
    </div>
  );
}
