# Budget Web

Next.js 16 (App Router) · React 19 · Tailwind v4 · shadcn/ui · Motion · TanStack Query · Serwist (PWA).

```bash
cp .env.example .env.local   # Supabase + URL da API
pnpm dev                     # http://localhost:3000
pnpm test                    # Vitest (lógica pura)
pnpm build && pnpm e2e       # Playwright (iPhone + desktop) — precisa da API rodando em :8000
```

| Pasta | Conteúdo |
|---|---|
| `src/app/(marketing)` | landing page |
| `src/app/(auth)` | entrar, cadastro, recuperar/redefinir senha |
| `src/app/(app)` | área logada — shell client-side (ver `docs/adr/0006`) |
| `src/components/motion` | primitivas de animação (número animado, swipe, progresso…) |
| `src/lib/api` | client tipado, hooks do TanStack Query, mutações offline |
| `src/lib/offline` | persistência do cache e da fila de escrita no IndexedDB |
| `e2e/` | testes Playwright + `mock-auth.mjs` (Supabase Auth falso para rodar sem Docker) |

Regras da casa: valores sempre em centavos (`<Money cents={…} />`), transações com ID gerado no
cliente (`newId()`) e gravadas com `PUT` idempotente, animações via `src/lib/motion.ts`.
