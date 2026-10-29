import type { Metadata } from "next";
import { SettingsView } from "./settings-view";

export const metadata: Metadata = { title: "Configurações" };

export default function ConfiguracoesPage() {
  return <SettingsView />;
}
