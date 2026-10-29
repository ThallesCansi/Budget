<div align="center">
  <img src="apps/web/public/brand/logo.svg" alt="Budget" width="220" />

  <p><strong>Controle financeiro pessoal e familiar — rápido, bonito e feito para o celular.</strong></p>

  <p>
    <a href="../../actions/workflows/ci-web.yml"><img alt="CI Web" src="../../actions/workflows/ci-web.yml/badge.svg" /></a>
    <a href="../../actions/workflows/ci-api.yml"><img alt="CI API" src="../../actions/workflows/ci-api.yml/badge.svg" /></a>
    <img alt="License" src="https://img.shields.io/badge/license-MIT-56ab91" />
  </p>
</div>

## Recursos

- 📱 **PWA mobile-first** — instale no celular, use offline; lançamentos sincronizam depois
- ⚡ **Lançamento rápido** — `mercado 45,90 ontem nubank` e pronto
- 💳 **Cartões e faturas**, **parcelas** e **recorrências**
- 🎯 **Metas** e **orçamentos por categoria** com alertas
- 👨‍👩‍👧 **Família compartilhada** — mesma casa, vários membros
- 🧾 Comprovantes pela câmera e importação de extrato (OFX/CSV)
- 🔔 Notificações push de vencimentos e limites
- 🔐 Login com e-mail e senha, Google ou link mágico

## Stack

| Camada | Tecnologia | Hospedagem |
|---|---|---|
| Web | Next.js 16 · React 19 · Tailwind v4 · shadcn/ui · Motion · TanStack Query · Serwist | Vercel |
| API | FastAPI · SQLAlchemy 2 · Alembic · Pydantic v2 | Render |
| Dados & Auth | Postgres · Supabase Auth · Supabase Storage | Supabase |

Arquitetura detalhada em [docs/architecture.md](docs/architecture.md) e decisões em [docs/adr](docs/adr).

## Estrutura

```
apps/
  web/            Next.js (PWA)
  api/            FastAPI
packages/
  api-client/     tipos + client gerados do OpenAPI da API
  tsconfig/       tsconfig compartilhado
docs/             arquitetura, deploy, ADRs
```

## Desenvolvimento

Pré-requisitos: Node 22+, [pnpm](https://pnpm.io) 10, [uv](https://docs.astral.sh/uv/) e Python 3.12.

```bash
pnpm install                 # dependências JS + hooks de git (lefthook)
(cd apps/api && uv sync)     # dependências Python
pnpm dev:local               # sobe tudo: Postgres embutido, auth simulado, API (:8000) e web (:3000)
```

Abra <http://localhost:3000> e entre com **qualquer e-mail e senha** — o `pnpm dev:local` usa um
Supabase Auth simulado (`apps/web/e2e/mock-auth.mjs`), então não precisa de Docker nem de conta no
Supabase. Use `pnpm dev:local --prod` para testar o build de produção (PWA instalável, modo offline).

Para desenvolver contra um projeto Supabase real, copie `apps/api/.env.example` e
`apps/web/.env.example` (para `.env` / `.env.local`), preencha as chaves e rode `pnpm dev`.

Comandos úteis:

| Comando | O que faz |
|---|---|
| `pnpm dev:local` | ambiente local completo, sem Docker |
| `pnpm dev` | web + API usando os `.env` |
| `pnpm --filter @budget/web e2e` | testes de ponta a ponta (Playwright) |
| `pnpm test` | testes (pytest + vitest) |
| `pnpm lint` / `pnpm typecheck` | Biome + Ruff / tsc + mypy |
| `pnpm codegen` | regenera o client TypeScript a partir da API |

## Contribuindo

Commits seguem [Conventional Commits](https://www.conventionalcommits.org/pt-br/) (`feat(web): …`, `fix(api): …`) — o
[release-please](https://github.com/googleapis/release-please) gera o changelog e as versões. Veja
[docs/contributing.md](docs/contributing.md).

## Licença

[MIT](LICENSE)
