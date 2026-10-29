"use client";

import { motion } from "motion/react";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";

interface ProgressBarProps {
  value: number; // 0..1 (values above 1 are clamped visually)
  color?: string;
  className?: string;
  /** Shift to warning/danger colors as the value approaches/exceeds 1. */
  thresholds?: boolean;
}

export function ProgressBar({ value, color, className, thresholds }: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(1, value));
  const fill = thresholds
    ? value >= 1
      ? "var(--expense)"
      : value >= 0.8
        ? "var(--warning)"
        : "var(--income)"
    : (color ?? "var(--primary)");
  return (
    <div
      className={cn("bg-muted h-2 overflow-hidden rounded-full", className)}
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={Math.round(value * 100)}
    >
      <motion.div
        className="h-full rounded-full"
        initial={{ width: 0 }}
        animate={{ width: `${clamped * 100}%`, backgroundColor: fill }}
        transition={spring.gentle}
      />
    </div>
  );
}
