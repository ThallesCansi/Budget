"use client";

import type { LucideIcon } from "lucide-react";
import { motion } from "motion/react";
import type { ReactNode } from "react";
import { spring } from "@/lib/motion";

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
}: {
  icon: LucideIcon;
  title: string;
  description: string;
  action?: ReactNode;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={spring.gentle}
      className="bg-card/50 flex flex-col items-center gap-3 rounded-2xl border border-dashed px-6 py-10 text-center"
    >
      <motion.span
        animate={{ y: [0, -6, 0] }}
        transition={{ repeat: Number.POSITIVE_INFINITY, duration: 3, ease: "easeInOut" }}
        className="bg-brand-gradient shadow-glow grid size-14 place-items-center rounded-2xl text-white"
      >
        <Icon className="size-7" />
      </motion.span>
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-muted-foreground max-w-xs text-sm">{description}</p>
      {action}
    </motion.div>
  );
}
