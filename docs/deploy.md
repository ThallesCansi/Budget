# Deploy

## 1. Supabase

1. Crie um projeto (região **us-east-1**).
2. **Authentication → Providers**: habilite *Email* (com confirmação) e *Google*
   (crie as credenciais OAuth no Google Cloud com o redirect `https://<projeto>.supabase.co/auth/v1/callback`).
3. **Authentication → URL Configuration**: *Site URL* = URL da Vercel; adicione
   `https://<app>.vercel.app/auth/callback` e `http://localhost:3000/auth/callback` em *Redirect URLs*.
4. **Authentication → Emails**: traduza os templates para PT-BR (confirmação, link mágico, recuperação).
5. Anote: Project URL, *publishable key* e a connection string do **Session pooler** (porta 5432).

## 2. API no Render

1. **New → Blueprint** apontando para este repositório (usa `render.yaml`).
2. Preencha as variáveis:
   - `DATABASE_URL` — connection string do Session pooler
   - `SUPABASE_URL` — `https://<projeto>.supabase.co`
   - `CORS_ORIGINS` — `https://<app>.vercel.app` (vírgula para várias)
   - `SENTRY_DSN` — opcional
3. As migrations rodam a cada boot (`alembic upgrade head`).

> Plano free: a instância dorme após 15 min sem uso. O PWA abre com o cache local e o cron diário
> da Vercel também acorda a API.

## 3. Web na Vercel

1. **Add New → Project**, importe o repositório e defina **Root Directory = `apps/web`**.
2. Variáveis:
   - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
   - `NEXT_PUBLIC_API_URL` — URL do Render
   - `CRON_SECRET` — o mesmo valor gerado no Render
3. Cada PR ganha um deploy de preview; `main` vai para produção.
