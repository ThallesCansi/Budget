"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { authErrorMessage } from "@/lib/auth-errors";
import { spring } from "@/lib/motion";
import { getSupabase } from "@/lib/supabase/client";
import { Field, PasswordField } from "./field";
import { Divider, GoogleButton } from "./google-button";
import { SentNotice } from "./sent-notice";

function strength(password: string) {
  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;
  return Math.min(score, 4);
}

const LEVELS = [
  { label: "Muito fraca", color: "var(--expense)" },
  { label: "Fraca", color: "var(--expense)" },
  { label: "Razoável", color: "var(--warning)" },
  { label: "Boa", color: "var(--income)" },
  { label: "Forte", color: "var(--income)" },
];

export function SignUpForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);
  const level = strength(password);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password.length < 8) return setError("A senha precisa ter pelo menos 8 caracteres.");
    setPending(true);
    setError(null);
    const { data, error } = await getSupabase().auth.signUp({
      email,
      password,
      options: {
        data: { full_name: name.trim() },
        emailRedirectTo: `${window.location.origin}/auth/callback?next=/inicio`,
      },
    });
    setPending(false);
    if (error) return setError(authErrorMessage(error.message));
    if (data.session) {
      router.replace("/inicio");
    } else setSent(true);
  };

  if (sent) return <SentNotice email={email} />;

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold">Crie sua conta</h1>
        <p className="text-muted-foreground">Leva menos de um minuto.</p>
      </div>
      <GoogleButton />
      <Divider />
      <form onSubmit={submit} className="space-y-4">
        <Field
          label="Nome"
          id="name"
          autoComplete="name"
          required
          maxLength={120}
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Field
          label="E-mail"
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <div className="space-y-2">
          <PasswordField
            label="Senha"
            id="password"
            autoComplete="new-password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {password && (
            <div className="flex items-center gap-2" aria-live="polite">
              <div className="flex flex-1 gap-1">
                {[0, 1, 2, 3].map((i) => (
                  <motion.span
                    key={i}
                    className="bg-muted h-1.5 flex-1 rounded-full"
                    animate={{ backgroundColor: i < level ? LEVELS[level]!.color : "var(--muted)" }}
                    transition={spring.gentle}
                  />
                ))}
              </div>
              <span className="text-muted-foreground w-20 text-right text-xs">
                {LEVELS[level]!.label}
              </span>
            </div>
          )}
        </div>
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
          className="bg-brand-gradient shadow-glow h-12 w-full text-base font-semibold text-white"
        >
          {pending ? "Criando…" : "Criar conta"}
        </Button>
        <p className="text-muted-foreground text-center text-xs">
          Ao criar a conta você concorda com os termos de uso.
        </p>
      </form>
      <p className="text-muted-foreground text-center text-sm">
        Já tem conta?{" "}
        <Link href="/entrar" className="text-primary dark:text-secondary font-semibold">
          Entrar
        </Link>
      </p>
    </div>
  );
}
