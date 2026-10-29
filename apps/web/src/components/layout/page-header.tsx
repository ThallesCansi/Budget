"use client";

import { Eye, EyeOff } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";
import { Coin } from "@/components/brand/logo";
import { usePrivacy } from "@/components/providers/privacy-provider";
import { Button } from "@/components/ui/button";
import { UserAvatar } from "@/components/user-avatar";
import { useMe } from "@/lib/api/queries";

interface PageHeaderProps {
  title: ReactNode;
  subtitle?: ReactNode;
  actions?: ReactNode;
}

export function PageHeader({ title, subtitle, actions }: PageHeaderProps) {
  const { hidden, toggle } = usePrivacy();
  const { data: me } = useMe();
  return (
    <header className="pt-safe flex items-center gap-3">
      <Coin className="size-9 md:hidden" />
      <div className="min-w-0 flex-1">
        <h1 className="truncate text-xl font-bold md:text-2xl">{title}</h1>
        {subtitle && <p className="text-muted-foreground truncate text-sm">{subtitle}</p>}
      </div>
      {actions}
      <Button
        variant="ghost"
        size="icon-lg"
        onClick={toggle}
        aria-pressed={hidden}
        aria-label={hidden ? "Mostrar valores" : "Esconder valores"}
        title={hidden ? "Mostrar valores" : "Esconder valores"}
      >
        {hidden ? <EyeOff /> : <Eye />}
      </Button>
      <Link href="/perfil" aria-label="Perfil" className="rounded-full">
        <UserAvatar name={me?.full_name ?? me?.email} src={me?.avatar_url} />
      </Link>
    </header>
  );
}
