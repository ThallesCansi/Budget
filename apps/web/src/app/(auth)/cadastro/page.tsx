import type { Metadata } from "next";
import { SignUpForm } from "@/components/auth/sign-up-form";

export const metadata: Metadata = { title: "Criar conta" };

export default function CadastroPage() {
  return <SignUpForm />;
}
