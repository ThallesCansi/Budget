"use client";

import { motion } from "motion/react";
import Image from "next/image";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";

const FEATURES = [
  {
    image: "/illustrations/functionalities1.svg",
    title: "Tudo num só lugar",
    text: "Dinheiro, contas bancárias, poupança e cartões de crédito com saldo sempre atualizado — e o patrimônio total num relance.",
  },
  {
    image: "/illustrations/functionalities2.svg",
    title: "Lance em segundos",
    text: "Teclado numérico feito para o polegar, categorias com um toque e funcionamento offline: o lançamento sincroniza quando a internet voltar.",
  },
  {
    image: "/illustrations/functionalities3.svg",
    title: "Entenda para onde vai o dinheiro",
    text: "Resumo do mês, gastos por categoria e lançamentos previstos para você saber o que ainda vai entrar e sair.",
  },
  {
    image: "/illustrations/functionalities4.svg",
    title: "Planeje com metas e orçamentos",
    text: "Limites por categoria com alertas e metas com acompanhamento de progresso.",
    soon: true,
  },
  {
    image: "/illustrations/functionalities5.svg",
    title: "No seu bolso, como um app",
    text: "Instale o Budget na tela inicial do celular. Abre na hora, tem modo escuro e um modo privacidade que esconde os valores.",
  },
];

export function Features() {
  return (
    <section id="funcionalidades" className="mx-auto max-w-6xl space-y-24 px-6 py-20 md:space-y-32">
      {FEATURES.map((f, i) => (
        <motion.div
          key={f.title}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.3 }}
          className={cn(
            "grid items-center gap-10 md:grid-cols-2",
            i % 2 === 1 && "md:[&>*:first-child]:order-2",
          )}
        >
          <motion.div
            variants={{
              hidden: { opacity: 0, x: i % 2 ? 60 : -60, rotate: i % 2 ? 3 : -3 },
              show: { opacity: 1, x: 0, rotate: 0, transition: spring.gentle },
            }}
            whileHover={{ scale: 1.03, rotate: i % 2 ? -1 : 1 }}
          >
            <Image
              src={f.image}
              alt=""
              width={520}
              height={420}
              loading="lazy"
              className="h-auto w-full"
            />
          </motion.div>
          <motion.div
            variants={{
              hidden: { opacity: 0, y: 30 },
              show: { opacity: 1, y: 0, transition: { ...spring.gentle, delay: 0.1 } },
            }}
            className="space-y-4"
          >
            <span className="text-brand-green text-sm font-semibold tracking-widest uppercase">
              0{i + 1}
            </span>
            <h2 className="text-brand-blue dark:text-blue-accent-100 text-3xl font-bold md:text-4xl">
              {f.title}
              {f.soon && (
                <span className="bg-brand-green/15 text-brand-green ml-3 rounded-full px-3 py-1 align-middle text-xs font-semibold">
                  em breve
                </span>
              )}
            </h2>
            <p className="text-muted-foreground text-lg">{f.text}</p>
          </motion.div>
        </motion.div>
      ))}
    </section>
  );
}
