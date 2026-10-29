import type { Metadata } from "next";
import { AccountsView } from "./accounts-view";

export const metadata: Metadata = { title: "Carteiras" };

export default function CarteirasPage() {
  return <AccountsView />;
}
