import type { Metadata } from "next";
import { TransactionsView } from "./transactions-view";

export const metadata: Metadata = { title: "Transações" };

export default function TransacoesPage() {
  return <TransactionsView />;
}
