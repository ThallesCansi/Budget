"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface ChipProps {
  selected: boolean;
  onClick: () => void;
  children: ReactNode;
  color?: string;
  className?: string;
}

export function Chip({ selected, onClick, children, color, className }: ChipProps) {
  return (
    <motion.button
      type="button"
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      aria-pressed={selected}
      style={selected && color ? { backgroundColor: color, borderColor: color } : undefined}
      className={cn(
        "inline-flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition-colors",
        selected
          ? "border-primary bg-primary text-primary-foreground"
          : "border-border bg-card text-foreground hover:bg-muted",
        className,
      )}
    >
      {children}
    </motion.button>
  );
}
