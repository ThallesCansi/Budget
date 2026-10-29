"use client";

import { motion, useMotionValue, useSpring, useTransform } from "motion/react";
import { initials } from "@/components/user-avatar";
import { spring } from "@/lib/motion";

const TEAM = [
  {
    name: "Daniella Mendes",
    role: "UI",
    text: "Estudante do técnico em informática do IFES, responsável pela UI do sistema.",
  },
  {
    name: "Suzana Sequim",
    role: "UI",
    text: "Estudante do técnico em informática do IFES, responsável pela UI do sistema.",
  },
  {
    name: "Thalles Cansi",
    role: "UX",
    text: "Estudante do IFES e apaixonado por jogos, responsável pela UX do sistema.",
  },
  {
    name: "Vinicius Girelli",
    role: "UX",
    text: "Estudante do IFES, responsável pela UX do sistema.",
  },
];

/** Card with a subtle 3D tilt that follows the pointer (replaces vanilla-tilt.js). */
function TiltCard({ children }: { children: React.ReactNode }) {
  const x = useMotionValue(0.5);
  const y = useMotionValue(0.5);
  const rotateX = useSpring(useTransform(y, [0, 1], [8, -8]), spring.gentle);
  const rotateY = useSpring(useTransform(x, [0, 1], [-8, 8]), spring.gentle);
  return (
    <motion.div
      style={{ rotateX, rotateY, transformPerspective: 800 }}
      onPointerMove={(e) => {
        if (e.pointerType !== "mouse") return;
        const rect = e.currentTarget.getBoundingClientRect();
        x.set((e.clientX - rect.left) / rect.width);
        y.set((e.clientY - rect.top) / rect.height);
      }}
      onPointerLeave={() => {
        x.set(0.5);
        y.set(0.5);
      }}
      variants={{
        hidden: { opacity: 0, y: 30 },
        show: { opacity: 1, y: 0, transition: spring.gentle },
      }}
      className="bg-card shadow-card rounded-3xl border p-6 text-center"
    >
      {children}
    </motion.div>
  );
}

export function Team() {
  return (
    <section id="quem-somos" className="bg-brand-gradient-vertical px-6 py-20">
      <div className="mx-auto max-w-6xl space-y-10">
        <h2 className="text-center text-3xl font-bold text-white md:text-4xl">Quem somos</h2>
        <motion.div
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.2 }}
          variants={{ show: { transition: { staggerChildren: 0.08 } } }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          {TEAM.map((p) => (
            <TiltCard key={p.name}>
              <span className="bg-brand-gradient shadow-glow mx-auto mb-4 grid size-20 place-items-center rounded-full text-2xl font-bold text-white">
                {initials(p.name)}
              </span>
              <h3 className="text-lg font-semibold">{p.name}</h3>
              <p className="text-brand-green mb-3 text-xs font-semibold tracking-widest uppercase">
                {p.role}
              </p>
              <p className="text-muted-foreground text-sm">{p.text}</p>
            </TiltCard>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
