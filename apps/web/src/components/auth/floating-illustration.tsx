"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";

export function FloatingIllustration({ children }: { children: ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24, scale: 0.96 }}
      animate={{ opacity: 1, y: [0, -12, 0], scale: 1 }}
      transition={{
        opacity: { duration: 0.6 },
        scale: { duration: 0.6 },
        y: { repeat: Number.POSITIVE_INFINITY, duration: 6, ease: "easeInOut" },
      }}
    >
      {children}
    </motion.div>
  );
}
