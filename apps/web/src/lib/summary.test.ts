import type { Category, Transaction } from "@budget/api-client";
import { describe, expect, it } from "vitest";
import { expensesByCategory, monthTotals } from "./summary";

const tx = (over: Partial<Transaction>): Transaction =>
  ({
    id: crypto.randomUUID(),
    kind: "expense",
    amount_cents: 100,
    paid: true,
    category_id: null,
    ...over,
  }) as Transaction;

describe("monthTotals", () => {
  it("separates paid and pending, ignores transfers", () => {
    const totals = monthTotals([
      tx({ kind: "income", amount_cents: 5000 }),
      tx({ kind: "income", amount_cents: 700, paid: false }),
      tx({ kind: "expense", amount_cents: 1200 }),
      tx({ kind: "expense", amount_cents: 300, paid: false }),
      tx({ kind: "transfer", amount_cents: 9999 }),
    ]);
    expect(totals).toEqual({
      income: 5000,
      expense: 1200,
      net: 3800,
      pendingIncome: 700,
      pendingExpense: 300,
    });
  });
});

describe("expensesByCategory", () => {
  it("groups, sorts and computes shares", () => {
    const food = { id: "food", name: "Mercado" } as Category;
    const fun = { id: "fun", name: "Lazer" } as Category;
    const result = expensesByCategory(
      [
        tx({ category_id: "food", amount_cents: 300 }),
        tx({ category_id: "fun", amount_cents: 100 }),
        tx({ category_id: "food", amount_cents: 100 }),
      ],
      [food, fun],
    );
    expect(result.map((r) => [r.category?.name, r.total, r.share])).toEqual([
      ["Mercado", 400, 0.8],
      ["Lazer", 100, 0.2],
    ]);
  });
});
