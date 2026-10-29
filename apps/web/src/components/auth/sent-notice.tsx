"use client";

import { MailCheck } from "lucide-react";
import { motion } from "motion/react";
import { spring } from "@/lib/motion";

export function SentNotice({ email, children }: { email: string; children?: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={spring.gentle}
      className="space-y-4 text-center"
    >
      <motion.span
        initial={{ rotate: -12, scale: 0.6 }}
        animate={{ rotate: 0, scale: 1 }}
        transition={spring.bouncy}
        className="bg-brand-gradient shadow-glow mx-auto grid size-16 place-items-center rounded-2xl text-white"
      >
        <MailCheck className="size-8" />
      </motion.span>
      <h1 className="text-2xl font-bold">Confira seu e-mail</h1>
      <p className="text-muted-foreground">
        Enviamos um link para <strong className="text-foreground">{email}</strong>. Abra-o neste
        aparelho para continuar.
      </p>
      {children}
    </motion.div>
  );
}
