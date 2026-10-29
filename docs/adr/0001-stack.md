# 0001. Stack

- **Status:**  FastAPI + Next.js + Supabase
- **Data:** 2026-10-28

## Contexto

Aceita

## Decisão

O projeto antigo (FastAPI + Jinja + SQLite) não rodava em ambientes serverless e misturava UI e regras. Queremos manter Python no backend e ter um front moderno e mobile-first.

## Consequências

API em FastAPI (Render), web em Next.js (Vercel), Postgres/Auth/Storage no Supabase. Monorepo com pnpm + Turborepo, Python gerenciado por uv.:Dois deploys para manter; o plano free do Render tem cold start (mitigado pelo PWA offline-first, ver ADR 0004).
