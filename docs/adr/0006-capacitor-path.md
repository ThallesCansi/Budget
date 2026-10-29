# 0006. Caminho para lojas via Capacitor

- **Status:** Proposta
- **Data:** 2026-10-28

## Contexto

Queremos publicar na App Store/Play Store no futuro sem reescrever o app.

## Decisão

A área logada é um shell client-side que conversa só com a API; o empacotamento com Capacitor poderá apontar para a URL de produção (server.url) ou para um export estático do shell.

## Consequências

Evitar dependências de Server Components/Server Actions na área logada.
