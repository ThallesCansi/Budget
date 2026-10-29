# Arquitetura

```
┌──────────── Vercel ────────────┐          ┌──────── Render ─────────┐
│ apps/web (Next.js PWA)         │  Bearer  │ apps/api (FastAPI)      │
│  Service worker + IndexedDB    ├─────────►│  valida JWT via JWKS    │
│  TanStack Query (cache+fila)   │   JWT    │  regras de negócio      │
│  Supabase Auth (sessão)        │          │  SQLAlchemy + Alembic   │
│  Cron diário ─► /internal/jobs │          │                         │
└───────────────┬────────────────┘          └────────────┬────────────┘
                │ login / sessão                          │ Postgres
                └──────────────► Supabase ◄───────────────┘
```

## Princípios

1. **O front só usa o Supabase para autenticação.** Todos os dados passam pela API, que é a única
   fonte de regras de negócio e de autorização.
2. **Isolamento por casa (household).** Toda linha de domínio tem `household_id`. A dependência
   `Ctx` resolve a casa ativa (header `X-Household-Id` ou padrão do perfil) e confirma que o usuário é
   membro; `get_owned()` responde 404 para recursos de outras casas.
3. **Defesa em profundidade.** As tabelas têm RLS habilitado sem policies: a Data API do Supabase
   (roles `anon`/`authenticated`) não enxerga nada. A API conecta como dona das tabelas.
4. **Dinheiro em centavos** (`BIGINT`), nunca ponto flutuante.
5. **Offline-first no cliente.** Transações têm ID gerado no cliente (UUID) e são gravadas com
   `PUT /v1/transactions/{id}` idempotente, então a fila offline pode reenviar sem duplicar.
6. **Contrato tipado.** O OpenAPI da API gera `packages/api-client`; a CI falha se ficar
   desatualizado.

## Regras de negócio

| Regra | Onde |
|---|---|
| Saldo = inicial + receitas − despesas ± transferências (só `paid`); `projected` inclui pendentes | `services/balances.py` |
| Compra no cartão no dia do fechamento ou depois → próxima fatura; fatura identificada pelo mês de vencimento | `services/invoices.py` |
| Primeiro acesso cria perfil, casa "Minha casa", carteira e categorias padrão (idempotente, seguro com concorrência) | `services/bootstrap.py` |

## Regiões

Supabase `us-east-1`, Render `virginia` e funções da Vercel em `iad1` — API e banco lado a lado.
