"use client";

import { ArrowRight, Receipt, TrendingDown, TrendingUp, Wallet } from "lucide-react";
import { motion } from "motion/react";
import Link from "next/link";
import { useMemo } from "react";
import { CategoryIcon } from "@/components/category-icon";
import { EmptyState } from "@/components/empty-state";
import { MonthSwitcher, MonthTransition } from "@/components/layout/month-switcher";
import { PageHeader } from "@/components/layout/page-header";
import { Money } from "@/components/money";
import { ProgressBar } from "@/components/motion/progress-bar";
import { Shimmer } from "@/components/motion/skeleton";
import { useMonth } from "@/components/providers/month-provider";
import { StatCard } from "@/components/stat-card";
import { TransactionRow } from "@/components/transactions/transaction-row";
import { useTransactionSheet } from "@/components/transactions/transaction-sheet";
import { Button } from "@/components/ui/button";
import {
  useAccounts,
  useCategories,
  useMe,
  useMonthTransactions,
  usePendingTransactionIds,
} from "@/lib/api/queries";
import { greeting } from "@/lib/format";
import { fadeUp, stagger } from "@/lib/motion";
import { expensesByCategory, monthTotals } from "@/lib/summary";

function Section({
  title,
  href,
  children,
}: {
  title: string;
  href?: string;
  children: React.ReactNode;
}) {
  return (
    <motion.section variants={fadeUp} className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">{title}</h2>
        {href && (
          <Link
            href={href}
            className="text-primary dark:text-secondary flex items-center gap-1 text-sm font-medium"
          >
            Ver tudo <ArrowRight className="size-4" />
          </Link>
        )}
      </div>
      {children}
    </motion.section>
  );
}

export function Dashboard() {
  const { month } = useMonth();
  const { data: me } = useMe();
  const { data: accounts } = useAccounts();
  const { data: categories = [] } = useCategories();
  const { data: transactions, isPending } = useMonthTransactions(month);
  const pendingIds = usePendingTransactionIds();
  const sheet = useTransactionSheet();

  const totals = useMemo(() => monthTotals(transactions ?? []), [transactions]);
  const spending = useMemo(
    () => expensesByCategory(transactions ?? [], categories).slice(0, 5),
    [transactions, categories],
  );
  const activeAccounts = (accounts ?? []).filter((a) => !a.archived);
  const balance = activeAccounts.reduce((sum, a) => sum + a.balance_cents, 0);
  const projected = activeAccounts.reduce((sum, a) => sum + a.projected_balance_cents, 0);
  const byId = useMemo(
    () => new Map([...(accounts ?? []).map((a) => [a.id, a] as const)]),
    [accounts],
  );
  const categoryById = useMemo(
    () => new Map(categories.map((c) => [c.id, c] as const)),
    [categories],
  );
  const firstName = me?.full_name?.split(" ")[0];

  return (
    <div className="space-y-6">
      <PageHeader
        title={firstName ? `${greeting()}, ${firstName}!` : `${greeting()}!`}
        subtitle="Aqui está o resumo das suas finanças"
      />

      <div className="flex justify-center md:justify-start">
        <MonthSwitcher />
      </div>

      <MonthTransition>
        <motion.div initial="hidden" animate="show" variants={stagger(0.06)} className="space-y-8">
          <div className="grid grid-cols-2 gap-3 md:grid-cols-3 md:gap-4">
            <StatCard
              label="saldo atual"
              cents={balance}
              icon={Wallet}
              tone="balance"
              className="col-span-2 md:col-span-1"
              hint={
                projected !== balance ? (
                  <>
                    previsto: <Money cents={projected} />
                  </>
                ) : undefined
              }
            />
            <StatCard
              label="receitas"
              cents={totals.income}
              icon={TrendingUp}
              tone="income"
              hint={
                totals.pendingIncome ? (
                  <>
                    + <Money cents={totals.pendingIncome} /> a receber
                  </>
                ) : undefined
              }
            />
            <StatCard
              label="despesas"
              cents={totals.expense}
              icon={TrendingDown}
              tone="expense"
              hint={
                totals.pendingExpense ? (
                  <>
                    + <Money cents={totals.pendingExpense} /> a pagar
                  </>
                ) : undefined
              }
            />
          </div>

          <div className="grid gap-8 lg:grid-cols-5">
            <div className="space-y-8 lg:col-span-3">
              <Section title="Transações recentes" href="/transacoes">
                {isPending && !transactions ? (
                  <div className="space-y-2">
                    {[0, 1, 2].map((i) => (
                      <Shimmer key={i} className="h-16" />
                    ))}
                  </div>
                ) : transactions?.length ? (
                  <div className="bg-card shadow-card divide-y overflow-hidden rounded-2xl border">
                    {transactions.slice(0, 6).map((t) => (
                      <TransactionRow
                        key={t.id}
                        transaction={t}
                        category={t.category_id ? categoryById.get(t.category_id) : undefined}
                        account={byId.get(t.account_id)}
                        toAccount={t.to_account_id ? byId.get(t.to_account_id) : undefined}
                        pending={pendingIds.has(t.id)}
                        onClick={() => sheet.edit(t)}
                      />
                    ))}
                  </div>
                ) : (
                  <EmptyState
                    icon={Receipt}
                    title="Nenhum lançamento neste mês"
                    description="Registre seus gastos e receitas para acompanhar para onde vai o seu dinheiro."
                    action={
                      <Button
                        onClick={() => sheet.create("expense")}
                        className="bg-brand-gradient mt-1 text-white"
                      >
                        Adicionar lançamento
                      </Button>
                    }
                  />
                )}
              </Section>
            </div>

            <div className="space-y-8 lg:col-span-2">
              <Section title="Para onde foi o dinheiro">
                {spending.length ? (
                  <ul className="bg-card shadow-card space-y-4 rounded-2xl border p-4">
                    {spending.map(({ category, total, share }) => (
                      <li key={category?.id ?? "none"} className="flex items-center gap-3">
                        <CategoryIcon icon={category?.icon} color={category?.color} size="sm" />
                        <div className="min-w-0 flex-1 space-y-1.5">
                          <div className="flex justify-between gap-2 text-sm">
                            <span className="truncate font-medium">
                              {category?.name ?? "Sem categoria"}
                            </span>
                            <Money cents={total} className="font-semibold" />
                          </div>
                          <ProgressBar value={share} color={category?.color} />
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="bg-card text-muted-foreground shadow-card rounded-2xl border p-4 text-sm">
                    Suas despesas por categoria aparecem aqui.
                  </p>
                )}
              </Section>

              <Section title="Suas contas" href="/carteiras">
                <div className="-mx-4 flex gap-3 overflow-x-auto px-4 pb-2 md:mx-0 md:grid md:overflow-visible md:px-0">
                  {activeAccounts.map((a) => (
                    <Link
                      key={a.id}
                      href="/carteiras"
                      className="bg-card shadow-card flex min-w-44 items-center gap-3 rounded-2xl border p-3 transition-transform hover:-translate-y-0.5"
                    >
                      <CategoryIcon icon={a.icon} color={a.color} />
                      <span className="min-w-0">
                        <span className="block truncate text-sm font-medium">{a.name}</span>
                        <Money
                          cents={a.balance_cents}
                          tone={a.balance_cents < 0 ? "expense" : "default"}
                          className="font-semibold"
                        />
                      </span>
                    </Link>
                  ))}
                </div>
              </Section>
            </div>
          </div>
        </motion.div>
      </MonthTransition>
    </div>
  );
}
