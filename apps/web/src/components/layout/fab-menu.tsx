"use client";

import type { TransactionKind } from "@budget/api-client";
import { ArrowLeftRight, Plus, TrendingDown, TrendingUp } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";
import { useTransactionSheet } from "@/components/transactions/transaction-sheet";
import { haptic } from "@/lib/haptics";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";

const ACTIONS: { kind: TransactionKind; label: string; icon: typeof Plus; className: string }[] = [
  { kind: "transfer", label: "Transferência", icon: ArrowLeftRight, className: "bg-transfer" },
  { kind: "income", label: "Receita", icon: TrendingUp, className: "bg-income" },
  { kind: "expense", label: "Despesa", icon: TrendingDown, className: "bg-expense" },
];

/**
 * The "+" from the original dashboard: expands into income / expense / transfer.
 * `variant="tab"` is the raised center button of the mobile tab bar.
 */
export function FabMenu({ variant }: { variant: "tab" | "floating" }) {
  const [open, setOpen] = useState(false);
  const sheet = useTransactionSheet();

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  const choose = (kind: TransactionKind) => {
    setOpen(false);
    sheet.create(kind);
  };

  return (
    <>
      <AnimatePresence>
        {open && (
          <motion.button
            type="button"
            aria-label="Fechar menu"
            className="fixed inset-0 z-40 bg-black/30 backdrop-blur-[2px]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setOpen(false)}
          />
        )}
      </AnimatePresence>

      <div className={cn("relative z-50", variant === "floating" && "fixed right-8 bottom-8")}>
        <AnimatePresence>
          {open && (
            <motion.ul
              className={cn(
                "absolute bottom-full mb-4 flex flex-col gap-3",
                variant === "tab" ? "left-1/2 -translate-x-1/2 items-center" : "right-0 items-end",
              )}
              initial="hidden"
              animate="show"
              exit="hidden"
              variants={{
                hidden: { transition: { staggerChildren: 0.03, staggerDirection: -1 } },
                show: { transition: { staggerChildren: 0.05, staggerDirection: -1 } },
              }}
            >
              {ACTIONS.map(({ kind, label, icon: Icon, className }) => (
                <motion.li
                  key={kind}
                  variants={{
                    hidden: { opacity: 0, y: 16, scale: 0.8 },
                    show: { opacity: 1, y: 0, scale: 1, transition: spring.bouncy },
                  }}
                >
                  <button
                    type="button"
                    onClick={() => choose(kind)}
                    className="flex items-center gap-3 whitespace-nowrap"
                  >
                    <span className="bg-card shadow-card rounded-full px-3 py-1.5 text-sm font-medium">
                      {label}
                    </span>
                    <span
                      className={cn(
                        "shadow-elevated grid size-12 place-items-center rounded-2xl text-white",
                        className,
                      )}
                    >
                      <Icon className="size-6" />
                    </span>
                  </button>
                </motion.li>
              ))}
            </motion.ul>
          )}
        </AnimatePresence>

        <motion.button
          type="button"
          aria-label={open ? "Fechar" : "Novo lançamento"}
          aria-expanded={open}
          onClick={() => {
            haptic();
            setOpen((v) => !v);
          }}
          whileTap={{ scale: 0.9 }}
          className={cn(
            "bg-brand-gradient shadow-glow grid place-items-center rounded-2xl text-white",
            variant === "tab" ? "-mt-7 size-14" : "size-16",
          )}
        >
          <motion.span animate={{ rotate: open ? 45 : 0 }} transition={spring.snappy}>
            <Plus className="size-7" strokeWidth={2.5} />
          </motion.span>
        </motion.button>
      </div>
    </>
  );
}
