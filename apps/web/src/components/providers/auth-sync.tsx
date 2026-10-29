"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { setActiveHousehold } from "@/lib/api/client";
import { clearPersistedCache } from "@/lib/offline/persister";
import { getSupabase } from "@/lib/supabase/client";

const LAST_USER_KEY = "budget:last-user";

/** Keeps the local cache scoped to the signed-in user: wipes it on sign-out or user switch. */
export function AuthSync() {
  const qc = useQueryClient();
  const router = useRouter();

  useEffect(() => {
    const wipe = async () => {
      qc.cancelQueries();
      qc.getMutationCache().clear();
      qc.clear();
      setActiveHousehold(null);
      await clearPersistedCache();
    };
    const { data } = getSupabase().auth.onAuthStateChange((event, session) => {
      const userId = session?.user.id ?? null;
      const lastUser = localStorage.getItem(LAST_USER_KEY);
      if (event === "SIGNED_OUT") {
        localStorage.removeItem(LAST_USER_KEY);
        void wipe().then(() => router.replace("/entrar"));
        return;
      }
      if (userId && lastUser && lastUser !== userId) void wipe();
      if (userId) localStorage.setItem(LAST_USER_KEY, userId);
    });
    return () => data.subscription.unsubscribe();
  }, [qc, router]);

  return null;
}
