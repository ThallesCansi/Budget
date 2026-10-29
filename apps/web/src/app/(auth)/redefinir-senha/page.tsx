"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";
import { PasswordField } from "@/components/auth/field";
import { Button } from "@/components/ui/button";
import { authErrorMessage } from "@/lib/auth-errors";
import { getSupabase } from "@/lib/supabase/client";

export default function RedefinirSenhaPage() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold">Nova senha</h1>
        <p className="text-muted-foreground">Escolha uma senha com pelo menos 8 caracteres.</p>
      </div>
      <form
        className="space-y-4"
        onSubmit={async (e) => {
          e.preventDefault();
          setPending(true);
          const { error } = await getSupabase().auth.updateUser({ password });
          setPending(false);
          if (error) return setError(authErrorMessage(error.message));
          toast.success("Senha alterada!");
          router.replace("/inicio");
        }}
      >
        <PasswordField
          label="Nova senha"
          id="password"
          autoComplete="new-password"
          required
          minLength={8}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
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
          Salvar nova senha
        </Button>
      </form>
    </div>
  );
}
