"use client";

import { AnimatedNumber } from "@/components/motion/animated-number";
import { formatMoney } from "@/lib/format";
import { cn } from "@/lib/utils";

const tones = {
  default: "",
  income: "text-income",
  expense: "text-expense",
  balance: "text-balance",
  muted: "text-muted-foreground",
  auto: "",
} as const;

interface MoneyProps {
  cents: number;
  tone?: keyof typeof tones;
  sign?: boolean;
  compact?: boolean;
  animate?: boolean;
  className?: string;
}

/** Amount in BRL. Marked with `data-money` so privacy mode can blur it. */
export function Money({ cents, tone = "default", sign, compact, animate, className }: MoneyProps) {
  const toneClass = tone === "auto" ? (cents < 0 ? "text-expense" : "text-income") : tones[tone];
  const format = (value: number) => formatMoney(value, { sign, compact });
  return (
    <span data-money className={cn("whitespace-nowrap", toneClass, className)}>
      {animate ? <AnimatedNumber value={cents} format={format} /> : format(cents)}
    </span>
  );
}
