"use client";

import { ChevronRight, LogOut, Settings, UserRound, Wallet } from "lucide-react";
import { motion } from "motion/react";
import Link from "next/link";
import { PageHeader } from "@/components/layout/page-header";
import { SignOutDialog } from "@/components/layout/sign-out-dialog";
import { ThemeToggle } from "@/components/theme-toggle";
import { fadeUp, stagger } from "@/lib/motion";

const LINKS = [
  { href: "/carteiras", label: "Carteiras e cartões", icon: Wallet },
  { href: "/configuracoes", label: "Configurações", icon: Settings },
  { href: "/perfil", label: "Perfil", icon: UserRound },
];

export default function MaisPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Mais" />
      <motion.ul
        initial="hidden"
        animate="show"
        variants={stagger()}
        className="bg-card shadow-card divide-y overflow-hidden rounded-2xl border"
      >
        {LINKS.map(({ href, label, icon: Icon }) => (
          <motion.li key={href} variants={fadeUp}>
            <Link
              href={href}
              className="active:bg-muted flex items-center gap-3 px-4 py-4 font-medium"
            >
              <Icon className="text-primary dark:text-secondary size-5" />
              <span className="flex-1">{label}</span>
              <ChevronRight className="text-muted-foreground size-4" />
            </Link>
          </motion.li>
        ))}
      </motion.ul>
      <ThemeToggle />
      <SignOutDialog>
        <button
          type="button"
          className="bg-card text-destructive flex w-full items-center justify-center gap-2 rounded-2xl border py-3 font-medium"
        >
          <LogOut className="size-5" /> Sair
        </button>
      </SignOutDialog>
    </div>
  );
}
