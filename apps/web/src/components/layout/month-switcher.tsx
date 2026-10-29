"use client";

import { isSameMonth } from "date-fns";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { AnimatePresence, motion, type PanInfo } from "motion/react";
import { useMonth } from "@/components/providers/month-provider";
import { Button } from "@/components/ui/button";
import { formatMonth } from "@/lib/format";
import { haptic } from "@/lib/haptics";
import { slide } from "@/lib/motion";

/** Month picker: arrows, or drag the label sideways (mobile). */
export function MonthSwitcher() {
  const { month, direction, shift, reset } = useMonth();
  const current = isSameMonth(month, new Date());

  const onDragEnd = (_: unknown, info: PanInfo) => {
    if (Math.abs(info.offset.x) < 40) return;
    haptic();
    shift(info.offset.x < 0 ? 1 : -1);
  };

  return (
    <div className="flex items-center gap-1">
      <Button variant="ghost" size="icon" aria-label="Mês anterior" onClick={() => shift(-1)}>
        <ChevronLeft />
      </Button>
      <div className="relative w-40 overflow-hidden text-center">
        <AnimatePresence mode="popLayout" initial={false} custom={direction}>
          <motion.button
            key={month.toISOString()}
            type="button"
            custom={direction}
            variants={slide}
            initial="enter"
            animate="center"
            exit="exit"
            drag="x"
            dragConstraints={{ left: 0, right: 0 }}
            dragElastic={0.4}
            onDragEnd={onDragEnd}
            onClick={current ? undefined : reset}
            title={current ? undefined : "Voltar para o mês atual"}
            className="w-full touch-pan-y py-1 font-semibold select-none"
          >
            {formatMonth(month)}
          </motion.button>
        </AnimatePresence>
      </div>
      <Button variant="ghost" size="icon" aria-label="Próximo mês" onClick={() => shift(1)}>
        <ChevronRight />
      </Button>
    </div>
  );
}

/** Wraps month-dependent content so it slides in the direction the user navigated. */
export function MonthTransition({ children }: { children: React.ReactNode }) {
  const { month, direction } = useMonth();
  return (
    <AnimatePresence mode="wait" initial={false} custom={direction}>
      <motion.div
        key={month.toISOString()}
        custom={direction}
        variants={slide}
        initial="enter"
        animate="center"
        exit="exit"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
