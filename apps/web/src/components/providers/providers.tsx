"use client";

import { PersistQueryClientProvider } from "@tanstack/react-query-persist-client";
import { MotionConfig } from "motion/react";
import { ThemeProvider } from "next-themes";
import { type ReactNode, useState } from "react";
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { makeQueryClient } from "@/lib/api/query-client";
import { persister } from "@/lib/offline/persister";
import { ApiStatus } from "./api-status";
import { AuthSync } from "./auth-sync";
import { PrivacyProvider } from "./privacy-provider";

const CACHE_MAX_AGE = 1000 * 60 * 60 * 24 * 7;

export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(makeQueryClient);

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      <PersistQueryClientProvider
        client={queryClient}
        persistOptions={{
          persister,
          maxAge: CACHE_MAX_AGE,
          buster: "v3",
          dehydrateOptions: { shouldDehydrateMutation: (m) => m.state.status === "pending" },
        }}
        // Show the restored cache instantly, replay unsent writes, then revalidate everything:
        // the persisted snapshot may predate the last changes made before the app closed.
        onSuccess={async () => {
          await queryClient.resumePausedMutations();
          await queryClient.invalidateQueries();
        }}
      >
        <MotionConfig reducedMotion="user">
          <PrivacyProvider>
            <TooltipProvider>{children}</TooltipProvider>
            <Toaster position="top-center" richColors closeButton />
            <ApiStatus />
            <AuthSync />
          </PrivacyProvider>
        </MotionConfig>
      </PersistQueryClientProvider>
    </ThemeProvider>
  );
}
