# Contribuindo

## Fluxo

1. Crie uma branch a partir de `main`: `feat/lancamento-rapido`, `fix/saldo-cartao`…
2. Commits no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/) — o hook
   `commit-msg` valida. Escopos: `web`, `api`, `ci`, `docs`.
3. Abra um PR. A CI roda apenas para as pastas alteradas.
4. Merge com *squash*. O release-please abre/atualiza o PR de release com o changelog.

## Organização do trabalho

- Um **milestone** por fase do roadmap; issues com labels `area:web`, `area:api`, `type:feat|fix|chore`.
- O quadro do GitHub Projects segue: Backlog → Em andamento → Review → Feito.

## Mudou a API?

```bash
pnpm codegen   # regenera packages/api-client a partir do OpenAPI
```

Mudou um modelo? Gere a migration:

```bash
cd apps/api && uv run alembic revision --autogenerate -m "descreva a mudança"
```
