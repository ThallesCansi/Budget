"use client";

import type { LucideIcon } from "lucide-react";
import { motion } from "motion/react";
import { Money } from "@/components/money";
import { fadeUp } from "@/lib/motion";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  cents: number;
  icon: LucideIcon;
  tone: "balance" | "income" | "expense";
  hint?: React.ReactNode;
  className?: string;
}

const toneBg = { balance: "bg-balance", income: "bg-income", expense: "bg-expense" } as const;

/** The three cards from the original dashboard (saldo / receita / despesa), now animated. */
export function StatCard({ label, cents, icon: Icon, tone, hint, className }: StatCardProps) {
  return (
    <motion.div
      variants={fadeUp}
      whileHover={{ y: -2 }}
      className={cn(
        "bg-card shadow-card flex flex-col gap-2 rounded-2xl border p-4 md:p-5",
        className,
      )}
    >
      <span
        className={cn(
          "shadow-elevated grid size-10 place-items-center rounded-xl text-white",
          toneBg[tone],
        )}
      >
        <Icon className="size-5" />
      </span>
      <Money
        cents={cents}
        tone={tone}
        animate
        className="text-2xl font-bold tracking-tight md:text-3xl"
      />
      <span className="text-muted-foreground text-sm">{label}</span>
      {hint && <span className="text-muted-foreground text-xs">{hint}</span>}
    </motion.div>
  );
}
