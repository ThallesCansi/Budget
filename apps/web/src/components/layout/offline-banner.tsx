"use client";

import { useIsMutating } from "@tanstack/react-query";
import { CloudOff, RefreshCw } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useOnline } from "@/hooks/use-online";

/** Shown only when it matters: offline, or with local writes still waiting to sync. */
export function OfflineBanner() {
  const online = useOnline();
  const pending = useIsMutating();
  const visible = !online || pending > 0;

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          className="overflow-hidden"
          role="status"
        >
          <div
            className={
              online
                ? "bg-muted text-muted-foreground flex items-center justify-center gap-2 px-4 py-1.5 text-xs"
                : "bg-warning flex items-center justify-center gap-2 px-4 py-1.5 text-xs font-medium text-black"
            }
          >
            {online ? (
              <>
                <RefreshCw className="size-3.5 animate-spin" /> Sincronizando {pending}{" "}
                {pending === 1 ? "alteração" : "alterações"}…
              </>
            ) : (
              <>
                <CloudOff className="size-3.5" /> Você está offline
                {pending > 0
                  ? ` — ${pending} ${pending === 1 ? "lançamento será enviado" : "lançamentos serão enviados"} depois`
                  : ""}
              </>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
