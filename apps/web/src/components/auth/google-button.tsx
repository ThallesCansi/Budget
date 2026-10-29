"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { authErrorMessage } from "@/lib/auth-errors";
import { getSupabase } from "@/lib/supabase/client";

function GoogleIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden className="size-5">
      <path
        fill="#4285F4"
        d="M23.5 12.27c0-.85-.08-1.67-.22-2.45H12v4.64h6.45a5.5 5.5 0 0 1-2.4 3.62v3h3.87c2.27-2.09 3.58-5.17 3.58-8.81Z"
      />
      <path
        fill="#34A853"
        d="M12 24c3.24 0 5.96-1.07 7.95-2.92l-3.87-3c-1.08.72-2.45 1.15-4.08 1.15-3.13 0-5.79-2.11-6.74-4.96h-4v3.09A12 12 0 0 0 12 24Z"
      />
      <path
        fill="#FBBC05"
        d="M5.26 14.27A7.2 7.2 0 0 1 4.88 12c0-.79.14-1.55.38-2.27V6.64h-4A12 12 0 0 0 0 12c0 1.94.46 3.77 1.28 5.36l3.98-3.09Z"
      />
      <path
        fill="#EA4335"
        d="M12 4.77c1.76 0 3.35.61 4.6 1.8l3.43-3.43A11.96 11.96 0 0 0 12 0 12 12 0 0 0 1.28 6.64l3.98 3.09C6.21 6.88 8.87 4.77 12 4.77Z"
      />
    </svg>
  );
}

export function GoogleButton({ next = "/inicio" }: { next?: string }) {
  const [pending, setPending] = useState(false);
  return (
    <Button
      type="button"
      variant="outline"
      size="lg"
      disabled={pending}
      className="h-12 w-full gap-3 text-base font-medium"
      onClick={async () => {
        setPending(true);
        const { error } = await getSupabase().auth.signInWithOAuth({
          provider: "google",
          options: {
            redirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
          },
        });
        if (error) {
          setPending(false);
          toast.error(authErrorMessage(error.message));
        }
      }}
    >
      <GoogleIcon /> Continuar com Google
    </Button>
  );
}

export function Divider() {
  return (
    <div className="text-muted-foreground flex items-center gap-3 text-xs">
      <span className="bg-border h-px flex-1" /> ou <span className="bg-border h-px flex-1" />
    </div>
  );
}
