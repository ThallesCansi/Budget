"use client";

import { Menu, X } from "lucide-react";
import { AnimatePresence, motion, useMotionValueEvent, useScroll } from "motion/react";
import Link from "next/link";
import { useState } from "react";
import { Logo } from "@/components/brand/logo";
import { cn } from "@/lib/utils";

const LINKS = [
  { href: "#inicio", label: "Início" },
  { href: "#funcionalidades", label: "Funcionalidades" },
  { href: "#quem-somos", label: "Quem somos" },
];

export function SiteHeader() {
  const { scrollY } = useScroll();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  useMotionValueEvent(scrollY, "change", (y) => setScrolled(y > 24));

  return (
    <header
      className={cn(
        "pt-safe fixed inset-x-0 top-0 z-50 transition-colors duration-500",
        scrolled ? "bg-brand-blue/90 shadow-elevated backdrop-blur-lg" : "bg-transparent",
      )}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" aria-label="Budget">
          <Logo className="h-10" priority light />
        </Link>
        <nav className="hidden items-center gap-8 font-semibold text-white md:flex">
          {LINKS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="opacity-85 transition-opacity hover:opacity-100"
            >
              {l.label}
            </a>
          ))}
          <Link
            href="/entrar"
            className="text-brand-blue rounded-full bg-white px-5 py-2 transition-transform hover:scale-105"
          >
            Entrar
          </Link>
        </nav>
        <button
          type="button"
          className="text-white md:hidden"
          onClick={() => setOpen((v) => !v)}
          aria-label="Menu"
          aria-expanded={open}
        >
          {open ? <X className="size-7" /> : <Menu className="size-7" />}
        </button>
      </div>
      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="bg-brand-blue overflow-hidden md:hidden"
          >
            <div className="flex flex-col gap-1 px-6 pb-6 font-semibold text-white">
              {LINKS.map((l) => (
                <a key={l.href} href={l.href} onClick={() => setOpen(false)} className="py-3">
                  {l.label}
                </a>
              ))}
              <Link
                href="/entrar"
                className="text-brand-blue mt-2 rounded-full bg-white py-3 text-center"
              >
                Entrar
              </Link>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}
