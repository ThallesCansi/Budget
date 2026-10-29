import type { Metadata } from "next";
import { ProfileView } from "./profile-view";

export const metadata: Metadata = { title: "Perfil" };

export default function PerfilPage() {
  return <ProfileView />;
}
