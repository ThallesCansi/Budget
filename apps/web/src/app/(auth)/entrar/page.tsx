import type { Metadata } from "next";
import { Suspense } from "react";
import { SignInForm } from "@/components/auth/sign-in-form";

export const metadata: Metadata = { title: "Entrar" };

export default function EntrarPage() {
  return (
    <Suspense>
      <SignInForm />
    </Suspense>
  );
}
