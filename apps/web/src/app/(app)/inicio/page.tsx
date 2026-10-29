import type { Metadata } from "next";
import { Dashboard } from "./dashboard";

export const metadata: Metadata = { title: "Início" };

export default function InicioPage() {
  return <Dashboard />;
}
