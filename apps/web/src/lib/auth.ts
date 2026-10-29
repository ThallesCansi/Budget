import { getSupabase } from "@/lib/supabase/client";

/** Signs out; <AuthSync> wipes the local cache and redirects to /entrar. */
export async function signOut() {
  await getSupabase().auth.signOut();
}
