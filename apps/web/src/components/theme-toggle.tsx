"use client";

import { Monitor, Moon, Sun } from "lucide-react";
import { motion } from "motion/react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";

const OPTIONS = [
  { value: "light", label: "Claro", icon: Sun },
  { value: "dark", label: "Escuro", icon: Moon },
  { value: "system", label: "Automático", icon: Monitor },
] as const;

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const current = mounted ? theme : undefined;

  return (
    <fieldset className="bg-muted grid min-w-0 grid-cols-3 rounded-xl p-1">
      <legend className="sr-only">Tema</legend>
      {OPTIONS.map(({ value, label, icon: Icon }) => (
        <button
          key={value}
          type="button"
          aria-pressed={current === value}
          onClick={() => setTheme(value)}
          className={cn(
            "relative flex items-center justify-center gap-1.5 rounded-lg py-2 text-sm font-medium transition-colors",
            current === value ? "text-foreground" : "text-muted-foreground",
          )}
        >
          {current === value && (
            <motion.span
              layoutId="theme-pill"
              className="bg-card shadow-card absolute inset-0 rounded-lg"
              transition={spring.snappy}
            />
          )}
          <Icon className="relative size-4" />
          <span className="relative">{label}</span>
        </button>
      ))}
    </fieldset>
  );
}
