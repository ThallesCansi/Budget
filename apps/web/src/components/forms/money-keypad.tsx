"use client";

import { Delete } from "lucide-react";
import { motion } from "motion/react";
import { haptic } from "@/lib/haptics";

const KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "00", "0", "back"] as const;
const MAX_CENTS = 99_999_999_99;

/** Applies a keypad key to an amount typed in cents from right to left ("1","2","3" -> R$ 1,23). */
export function applyKey(cents: number, key: string): number {
  if (key === "back") return Math.floor(cents / 10);
  const next = Number(`${cents}${key}`);
  return next > MAX_CENTS ? cents : next;
}

export function MoneyKeypad({
  value,
  onChange,
}: {
  value: number;
  onChange: (cents: number) => void;
}) {
  return (
    <fieldset className="grid min-w-0 grid-cols-3 gap-2">
      <legend className="sr-only">Teclado numérico</legend>
      {KEYS.map((key) => (
        <motion.button
          key={key}
          type="button"
          whileTap={{ scale: 0.92 }}
          onClick={() => {
            haptic();
            onChange(applyKey(value, key));
          }}
          onContextMenu={(e) => {
            if (key !== "back") return;
            e.preventDefault();
            onChange(0);
          }}
          aria-label={key === "back" ? "Apagar" : key}
          className="bg-muted active:bg-accent flex h-13 items-center justify-center rounded-xl text-xl font-semibold"
        >
          {key === "back" ? <Delete className="size-5" /> : key}
        </motion.button>
      ))}
    </fieldset>
  );
}
