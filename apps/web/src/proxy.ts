import { createServerClient } from "@supabase/ssr";
import { type NextRequest, NextResponse } from "next/server";
import { env } from "@/lib/env";

const APP_PREFIXES = [
  "/inicio",
  "/transacoes",
  "/carteiras",
  "/planejamento",
  "/configuracoes",
  "/perfil",
  "/mais",
];
const GUEST_ONLY = ["/entrar", "/cadastro"];

const matches = (path: string, prefixes: string[]) =>
  prefixes.some((p) => path === p || path.startsWith(`${p}/`));

/** Refreshes the Supabase session cookie and guards private/guest-only routes. */
export async function proxy(request: NextRequest) {
  // Router prefetches only fetch static shells (no data). Leave them untouched: rewriting their
  // headers (session refresh) or redirecting them makes Next answer 404. The real navigation
  // that follows still goes through the checks below.
  if (request.headers.has("next-router-prefetch")) return NextResponse.next();

  // Refreshed session cookies only go on the response. No Server Component reads the session
  // (the signed-in area is client-side), and forwarding modified request headers stops Next from
  // serving the prerendered RSC payloads (404s right after sign-in).
  const response = NextResponse.next();

  const supabase = createServerClient(env.supabaseUrl, env.supabaseKey, {
    cookies: {
      getAll: () => request.cookies.getAll(),
      setAll: (toSet) => {
        for (const { name, value, options } of toSet) response.cookies.set(name, value, options);
      },
    },
  });

  // getClaims() validates the JWT (and refreshes it when needed) — never trust getSession() here.
  const { data } = await supabase.auth.getClaims();
  const signedIn = Boolean(data?.claims);
  const path = request.nextUrl.pathname;

  if (!signedIn && matches(path, APP_PREFIXES)) {
    const url = request.nextUrl.clone();
    url.pathname = "/entrar";
    url.search = `?next=${encodeURIComponent(path + request.nextUrl.search)}`;
    return NextResponse.redirect(url);
  }
  if (signedIn && matches(path, GUEST_ONLY)) {
    const url = request.nextUrl.clone();
    url.pathname = "/inicio";
    url.search = "";
    return NextResponse.redirect(url);
  }
  return response;
}

export const config = {
  matcher: [
    // Everything except static assets, the service worker and PWA files.
    "/((?!_next/static|_next/image|serwist|brand|illustrations|icons|manifest.webmanifest|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};
