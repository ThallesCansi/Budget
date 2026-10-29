# Budget API

FastAPI + SQLAlchemy 2 + Alembic, autenticada pelos JWTs do Supabase Auth.

```bash
uv sync                                   # instala dependências
cp .env.example .env                      # configure DATABASE_URL / SUPABASE_URL
uv run alembic upgrade head               # aplica migrations
uv run fastapi dev app/main.py            # http://localhost:8000/docs
uv run pytest                             # testes (sobe um Postgres embutido se não houver TEST_DATABASE_URL)
```

Estrutura:

| Pasta | Conteúdo |
|---|---|
| `app/core` | config, banco, segurança (JWT/JWKS), dependências (`Ctx` = casa ativa) e erros |
| `app/models` | modelos SQLAlchemy (todas as tabelas) |
| `app/schemas` | contratos Pydantic de entrada/saída |
| `app/services` | regras de negócio (saldos, faturas, bootstrap…) |
| `app/routers` | endpoints `/v1/*` |
| `alembic/` | migrations |

Convenções: dinheiro sempre em centavos (`*_cents`, inteiro); todo recurso pertence a uma casa
(`household_id`) e é acessado via `get_owned`, que responde 404 para recursos de outras casas.
