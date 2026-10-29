import { createBrowserClient } from "@supabase/ssr";
import type { SupabaseClient } from "@supabase/supabase-js";
import { env } from "@/lib/env";

let client: SupabaseClient | undefined;

/** Browser Supabase client (singleton). Used only for authentication. */
export function getSupabase(): SupabaseClient {
  client ??= createBrowserClient(env.supabaseUrl, env.supabaseKey);
  return client;
}
