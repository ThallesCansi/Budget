"use client";

import { AnimatePresence, motion } from "motion/react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { authErrorMessage } from "@/lib/auth-errors";
import { spring } from "@/lib/motion";
import { getSupabase } from "@/lib/supabase/client";
import { cn } from "@/lib/utils";
import { Field, PasswordField } from "./field";
import { Divider, GoogleButton } from "./google-button";
import { SentNotice } from "./sent-notice";

type Mode = "password" | "magic";

const safeNext = (value: string | null) =>
  value?.startsWith("/") && !value.startsWith("//") ? value : "/inicio";

export function SignInForm() {
  const router = useRouter();
  const next = safeNext(useSearchParams().get("next"));
  const [mode, setMode] = useState<Mode>("password");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sent, setSent] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPending(true);
    setError(null);
    const supabase = getSupabase();
    if (mode === "password") {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) {
        setPending(false);
        return setError(authErrorMessage(error.message));
      }
      router.replace(next);
      return;
    }
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
        shouldCreateUser: true,
      },
    });
    setPending(false);
    if (error) return setError(authErrorMessage(error.message));
    setSent(true);
  };

  if (sent) {
    return (
      <SentNotice email={email}>
        <Button variant="ghost" onClick={() => setSent(false)}>
          Usar outro e-mail
        </Button>
      </SentNotice>
    );
  }

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold">Bem-vindo de volta</h1>
        <p className="text-muted-foreground">Entre para ver suas finanças.</p>
      </div>

      <GoogleButton next={next} />
      <Divider />

      <div className="bg-muted grid grid-cols-2 rounded-full p-1" role="tablist">
        {(
          [
            ["password", "Com senha"],
            ["magic", "Link mágico"],
          ] as const
        ).map(([value, label]) => (
          <button
            key={value}
            type="button"
            role="tab"
            aria-selected={mode === value}
            onClick={() => {
              setMode(value);
              setError(null);
            }}
            className={cn(
              "relative rounded-full py-2 text-sm font-medium",
              mode === value ? "text-foreground" : "text-muted-foreground",
            )}
          >
            {mode === value && (
              <motion.span
                layoutId="auth-mode"
                className="bg-card shadow-card absolute inset-0 rounded-full"
                transition={spring.snappy}
              />
            )}
            <span className="relative">{label}</span>
          </button>
        ))}
      </div>

      <form onSubmit={submit} className="space-y-4">
        <Field
          label="E-mail"
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <AnimatePresence initial={false} mode="popLayout">
          {mode === "password" ? (
            <motion.div
              key="password"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-2 overflow-hidden"
            >
              <PasswordField
                label="Senha"
                id="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Link
                href="/recuperar-senha"
                className="text-primary dark:text-secondary block text-right text-sm font-medium"
              >
                Esqueci minha senha
              </Link>
            </motion.div>
          ) : (
            <motion.p
              key="magic"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-muted-foreground text-sm"
            >
              Enviaremos um link para você entrar sem senha.
            </motion.p>
          )}
        </AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: [8, -6, 4, 0] }}
            role="alert"
            className="bg-destructive/10 text-destructive rounded-lg px-3 py-2 text-sm"
          >
            {error}
          </motion.p>
        )}
        <Button
          type="submit"
          size="lg"
          disabled={pending}
          className="bg-brand-gradient shadow-glow h-12 w-full text-base font-semibold text-white"
        >
          {pending ? "Aguarde…" : mode === "password" ? "Entrar" : "Enviar link"}
        </Button>
      </form>

      <p className="text-muted-foreground text-center text-sm">
        Ainda não tem conta?{" "}
        <Link href="/cadastro" className="text-primary dark:text-secondary font-semibold">
          Criar conta grátis
        </Link>
      </p>
    </div>
  );
}
