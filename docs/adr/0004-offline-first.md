# 0004. Offline-first no cliente

- **Status:** Aceita
- **Data:** 2026-10-28

## Contexto

O app é usado no celular, muitas vezes com conexão ruim, e a API no plano free tem cold start de até 50s.

## Decisão

Cache do TanStack Query persistido no IndexedDB; mutações otimistas em fila persistida; transações com UUID gerado no cliente e PUT idempotente; service worker (Serwist) para o shell.

## Consequências

Abertura instantânea e lançamentos offline. Conflitos resolvidos por last-write-wins.
