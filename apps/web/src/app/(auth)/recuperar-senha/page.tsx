"use client";

import Link from "next/link";
import { useState } from "react";
import { Field } from "@/components/auth/field";
import { SentNotice } from "@/components/auth/sent-notice";
import { Button } from "@/components/ui/button";
import { authErrorMessage } from "@/lib/auth-errors";
import { getSupabase } from "@/lib/supabase/client";

export default function RecuperarSenhaPage() {
  const [email, setEmail] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);

  if (sent) return <SentNotice email={email} />;

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold">Recuperar senha</h1>
        <p className="text-muted-foreground">Enviaremos um link para você criar uma nova senha.</p>
      </div>
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          setPending(true);
          const { error } = await getSupabase().auth.resetPasswordForEmail(email, {
            redirectTo: `${window.location.origin}/auth/callback?next=/redefinir-senha`,
          });
          setPending(false);
          if (error) setError(authErrorMessage(error.message));
          else setSent(true);
        }}
      >
        <Field
          label="E-mail"
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {error && (
          <p
            role="alert"
            className="bg-destructive/10 text-destructive rounded-lg px-3 py-2 text-sm"
          >
            {error}
          </p>
        )}
        <Button
          type="submit"
          size="lg"
          disabled={pending}
          className="bg-brand-gradient h-12 w-full text-base font-semibold text-white"
        >
          Enviar link
        </Button>
      </form>
      <Link
        href="/entrar"
        className="text-primary dark:text-secondary block text-center text-sm font-medium"
      >
        Voltar para o login
      </Link>
    </div>
  );
}
