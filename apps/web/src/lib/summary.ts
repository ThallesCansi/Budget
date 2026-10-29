import type { Category, Transaction } from "@budget/api-client";

export interface MonthTotals {
  income: number;
  expense: number;
  net: number;
  pendingIncome: number;
  pendingExpense: number;
}

/** Month totals computed on the client, so they stay correct offline and update optimistically. */
export function monthTotals(transactions: Transaction[]): MonthTotals {
  const totals = { income: 0, expense: 0, pendingIncome: 0, pendingExpense: 0 };
  for (const t of transactions) {
    if (t.kind === "income") totals[t.paid ? "income" : "pendingIncome"] += t.amount_cents;
    if (t.kind === "expense") totals[t.paid ? "expense" : "pendingExpense"] += t.amount_cents;
  }
  return { ...totals, net: totals.income - totals.expense };
}

export interface CategorySpend {
  category: Category | undefined;
  total: number;
  share: number;
}

export function expensesByCategory(
  transactions: Transaction[],
  categories: Category[],
): CategorySpend[] {
  const byId = new Map(categories.map((c) => [c.id, c]));
  const totals = new Map<string, number>();
  let sum = 0;
  for (const t of transactions) {
    if (t.kind !== "expense") continue;
    const key = t.category_id ?? "none";
    totals.set(key, (totals.get(key) ?? 0) + t.amount_cents);
    sum += t.amount_cents;
  }
  return [...totals.entries()]
    .map(([id, total]) => ({ category: byId.get(id), total, share: sum ? total / sum : 0 }))
    .sort((a, b) => b.total - a.total);
}
