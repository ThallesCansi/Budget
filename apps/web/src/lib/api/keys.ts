export const qk = {
  me: ["me"] as const,
  accounts: ["accounts"] as const,
  categories: ["categories"] as const,
  transactions: ["transactions"] as const,
  month: (month: string) => ["transactions", "month", month] as const,
  transaction: (id: string) => ["transactions", "one", id] as const,
};

export const mk = {
  putTransaction: ["transactions", "put"] as const,
  deleteTransaction: ["transactions", "delete"] as const,
};
