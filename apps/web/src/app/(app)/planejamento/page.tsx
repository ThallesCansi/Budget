"use client";

import { PiggyBank, Target } from "lucide-react";
import { motion } from "motion/react";
import { PageHeader } from "@/components/layout/page-header";
import { ProgressBar } from "@/components/motion/progress-bar";
import { fadeUp, stagger } from "@/lib/motion";

const PREVIEW = [
  { name: "Mercado", value: 0.62 },
  { name: "Restaurantes", value: 0.86 },
  { name: "Lazer", value: 1.04 },
];

export default function PlanejamentoPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Planejamento" subtitle="Metas e orçamentos" />
      <motion.div
        initial="hidden"
        animate="show"
        variants={stagger(0.08)}
        className="grid gap-4 md:grid-cols-2"
      >
        <motion.div
          variants={fadeUp}
          className="bg-card shadow-card space-y-4 rounded-2xl border p-5"
        >
          <div className="flex items-center gap-3">
            <span className="bg-brand-gradient grid size-10 place-items-center rounded-xl text-white">
              <PiggyBank className="size-5" />
            </span>
            <div>
              <h2 className="font-semibold">Orçamentos por categoria</h2>
              <p className="text-muted-foreground text-sm">Em breve</p>
            </div>
          </div>
          <ul className="space-y-3 opacity-80">
            {PREVIEW.map((p) => (
              <li key={p.name} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span>{p.name}</span>
                  <span className="text-muted-foreground">{Math.round(p.value * 100)}%</span>
                </div>
                <ProgressBar value={p.value} thresholds />
              </li>
            ))}
          </ul>
        </motion.div>
        <motion.div
          variants={fadeUp}
          className="bg-card shadow-card space-y-3 rounded-2xl border p-5"
        >
          <div className="flex items-center gap-3">
            <span className="bg-secondary grid size-10 place-items-center rounded-xl text-white">
              <Target className="size-5" />
            </span>
            <div>
              <h2 className="font-semibold">Metas</h2>
              <p className="text-muted-foreground text-sm">Em breve</p>
            </div>
          </div>
          <p className="text-muted-foreground text-sm">
            Defina objetivos como "Viagem de férias" ou "Reserva de emergência", registre aportes e
            acompanhe o progresso — com comemoração quando chegar lá.
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
}
