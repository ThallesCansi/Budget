"use client";

import { addMonths, startOfMonth } from "date-fns";
import { createContext, type ReactNode, useCallback, useContext, useState } from "react";

interface MonthContextValue {
  month: Date;
  /** +1 forward, -1 back — drives the slide direction of month transitions. */
  direction: number;
  shift: (delta: number) => void;
  reset: () => void;
}

const MonthContext = createContext<MonthContextValue | null>(null);

/** The month being viewed, shared by dashboard and transactions. */
export function MonthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState(() => ({ month: startOfMonth(new Date()), direction: 0 }));
  const shift = useCallback(
    (delta: number) => setState((s) => ({ month: addMonths(s.month, delta), direction: delta })),
    [],
  );
  const reset = useCallback(
    () =>
      setState((s) => {
        const current = startOfMonth(new Date());
        return { month: current, direction: current > s.month ? 1 : -1 };
      }),
    [],
  );
  return <MonthContext value={{ ...state, shift, reset }}>{children}</MonthContext>;
}

export function useMonth() {
  const ctx = useContext(MonthContext);
  if (!ctx) throw new Error("useMonth must be used within MonthProvider");
  return ctx;
}
