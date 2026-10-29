"use client";

import { useState } from "react";
import { toast } from "sonner";
import { PageHeader } from "@/components/layout/page-header";
import { SettingsSection } from "@/components/settings-section";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { UserAvatar } from "@/components/user-avatar";
import { useMe, useUpdateMe } from "@/lib/api/queries";
import { getSupabase } from "@/lib/supabase/client";

function NameForm({ initial }: { initial: string }) {
  const [name, setName] = useState(initial);
  const update = useUpdateMe();
  return (
    <form
      className="flex items-end gap-2"
      onSubmit={(e) => {
        e.preventDefault();
        update.mutate(
          { full_name: name.trim() },
          { onSuccess: () => toast.success("Nome atualizado") },
        );
      }}
    >
      <div className="flex-1 space-y-1.5">
        <Label htmlFor="name">Nome</Label>
        <Input
          id="name"
          required
          maxLength={120}
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="h-11 text-base"
        />
      </div>
      <Button
        type="submit"
        size="lg"
        className="h-11"
        disabled={update.isPending || name.trim() === initial}
      >
        Salvar
      </Button>
    </form>
  );
}

function PasswordForm() {
  const [password, setPassword] = useState("");
  const [pending, setPending] = useState(false);
  return (
    <form
      className="flex items-end gap-2"
      onSubmit={async (e) => {
        e.preventDefault();
        setPending(true);
        const { error } = await getSupabase().auth.updateUser({ password });
        setPending(false);
        if (error) toast.error(error.message);
        else {
          setPassword("");
          toast.success("Senha alterada");
        }
      }}
    >
      <div className="flex-1 space-y-1.5">
        <Label htmlFor="new-password">Nova senha</Label>
        <Input
          id="new-password"
          type="password"
          autoComplete="new-password"
          minLength={8}
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="h-11 text-base"
        />
      </div>
      <Button type="submit" size="lg" className="h-11" disabled={pending}>
        Alterar
      </Button>
    </form>
  );
}

export function ProfileView() {
  const { data: me } = useMe();
  return (
    <div className="space-y-8">
      <PageHeader title="Perfil" />
      <div className="flex flex-col items-center gap-3 text-center">
        <UserAvatar
          name={me?.full_name ?? me?.email}
          src={me?.avatar_url}
          className="size-24 text-2xl"
        />
        <div>
          <p className="text-xl font-semibold">{me?.full_name ?? "—"}</p>
          <p className="text-muted-foreground text-sm">{me?.email}</p>
        </div>
      </div>
      <div className="mx-auto max-w-xl space-y-8">
        <SettingsSection title="Dados pessoais">
          {me && <NameForm key={me.full_name} initial={me.full_name ?? ""} />}
        </SettingsSection>
        <SettingsSection
          title="Segurança"
          description="Entrou com Google ou link mágico? Você pode criar uma senha aqui também."
        >
          <PasswordForm />
        </SettingsSection>
        {me && (
          <SettingsSection title="Casa">
            <p className="font-medium">{me.household.name}</p>
            <p className="text-muted-foreground text-sm">
              {me.household.members.map((m) => m.display_name).join(", ")}
            </p>
          </SettingsSection>
        )}
      </div>
    </div>
  );
}
