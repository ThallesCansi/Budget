"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { type ReactNode, Suspense, useEffect } from "react";
import { MonthProvider } from "@/components/providers/month-provider";
import {
  TransactionSheetProvider,
  useTransactionSheet,
} from "@/components/transactions/transaction-sheet";
import { useIsClient } from "@/hooks/use-is-client";
import { BottomNav } from "./bottom-nav";
import { FabMenu } from "./fab-menu";
import { OfflineBanner } from "./offline-banner";
import { ShellSkeleton } from "./shell-skeleton";
import { Sidebar } from "./sidebar";

/** Opens the transaction sheet from PWA shortcuts (`/inicio?novo=expense`). */
function ShortcutHandler() {
  const params = useSearchParams();
  const router = useRouter();
  const sheet = useTransactionSheet();
  const novo = params.get("novo");
  useEffect(() => {
    if (novo === "expense" || novo === "income" || novo === "transfer") {
      sheet.create(novo);
      router.replace(window.location.pathname);
    }
  }, [novo, sheet, router]);
  return null;
}

/**
 * The signed-in area is a client-side app shell (see docs/adr/0006): data lives in the local
 * cache, so only a static skeleton is prerendered and the UI mounts after hydration.
 */
export function AppShell({ children }: { children: ReactNode }) {
  const isClient = useIsClient();
  if (!isClient) return <ShellSkeleton />;
  return (
    <MonthProvider>
      <TransactionSheetProvider>
        <Sidebar />
        <div className="md:pl-20 lg:pl-64">
          <div className="sticky top-0 z-20">
            <OfflineBanner />
          </div>
          <main className="mx-auto w-full max-w-6xl px-4 pt-4 pb-28 md:px-8 md:pt-8 md:pb-12">
            {children}
          </main>
        </div>
        <BottomNav />
        <div className="hidden md:block">
          <FabMenu variant="floating" />
        </div>
        <Suspense>
          <ShortcutHandler />
        </Suspense>
      </TransactionSheetProvider>
    </MonthProvider>
  );
}
