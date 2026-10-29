"use client";

import { ArrowRight } from "lucide-react";
import { motion, useScroll, useTransform } from "motion/react";
import Image from "next/image";
import Link from "next/link";
import { useRef } from "react";
import { spring } from "@/lib/motion";

export function Hero() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], [0, 120]);
  const opacity = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

  return (
    <section
      ref={ref}
      id="inicio"
      className="bg-brand-gradient-vertical relative overflow-hidden pt-28 pb-20 text-white md:pt-36"
    >
      <div className="mx-auto grid max-w-6xl items-center gap-12 px-6 md:grid-cols-2">
        <motion.div style={{ opacity }} className="space-y-6">
          <motion.h1
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={spring.gentle}
            className="text-4xl leading-tight font-bold md:text-5xl"
          >
            Organize suas finanças de forma <u className="decoration-green-accent-300">fácil</u>,{" "}
            <u className="decoration-green-accent-300">prática</u> e{" "}
            <u className="decoration-green-accent-300">segura</u> com o{" "}
            <span className="text-green-accent-200">Budget</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...spring.gentle, delay: 0.1 }}
            className="max-w-lg text-lg text-white/85"
          >
            Pelo celular ou pelo computador, tenha controle de tudo o que acontece com o seu
            dinheiro — até sem internet.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...spring.gentle, delay: 0.2 }}
            className="flex flex-wrap gap-3"
          >
            <Link
              href="/cadastro"
              className="group text-brand-blue shadow-elevated inline-flex items-center gap-2 rounded-full bg-white px-6 py-3 font-semibold transition-transform hover:scale-105"
            >
              Criar conta grátis{" "}
              <ArrowRight className="size-5 transition-transform group-hover:translate-x-1" />
            </Link>
            <Link
              href="/entrar"
              className="rounded-full border-2 border-white/40 px-6 py-3 font-semibold transition-colors hover:bg-white/10"
            >
              Já tenho conta
            </Link>
          </motion.div>
        </motion.div>
        <motion.div
          style={{ y }}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ ...spring.gentle, delay: 0.15 }}
        >
          <motion.div
            animate={{ y: [0, -14, 0] }}
            transition={{ repeat: Number.POSITIVE_INFINITY, duration: 6, ease: "easeInOut" }}
          >
            <Image
              src="/illustrations/header.svg"
              alt="Ilustração do Budget"
              width={560}
              height={450}
              priority
              className="h-auto w-full drop-shadow-2xl"
            />
          </motion.div>
        </motion.div>
      </div>
      <svg
        className="text-background absolute inset-x-0 -bottom-px w-full"
        viewBox="0 0 1440 80"
        preserveAspectRatio="none"
        aria-hidden
      >
        <path fill="currentColor" d="M0 80V40c240-40 480-40 720 0s480 40 720 0v40Z" />
      </svg>
    </section>
  );
}
