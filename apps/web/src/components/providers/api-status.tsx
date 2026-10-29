"use client";

import { useEffect } from "react";
import { toast } from "sonner";
import { API_READY_EVENT, API_SLOW_EVENT } from "@/lib/api/client";

const TOAST_ID = "api-waking";

/** Tells the user the (free-tier) API is waking up instead of leaving them staring at a spinner. */
export function ApiStatus() {
  useEffect(() => {
    let showing = false;
    const onSlow = () => {
      if (showing) return;
      showing = true;
      toast.loading("Acordando o servidor…", {
        id: TOAST_ID,
        description:
          "O primeiro acesso depois de um tempo leva alguns segundos. Seus dados já estão na tela.",
        duration: Number.POSITIVE_INFINITY,
      });
    };
    const onReady = () => {
      if (!showing) return;
      showing = false;
      toast.success("Tudo sincronizado", { id: TOAST_ID, description: undefined, duration: 1500 });
    };
    window.addEventListener(API_SLOW_EVENT, onSlow);
    window.addEventListener(API_READY_EVENT, onReady);
    return () => {
      window.removeEventListener(API_SLOW_EVENT, onSlow);
      window.removeEventListener(API_READY_EVENT, onReady);
    };
  }, []);
  return null;
}
