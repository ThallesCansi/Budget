# 0002. Autenticação pelo Supabase, autorização na API

- **Status:** Aceita
- **Data:** 2026-10-28

## Contexto

Precisamos de e-mail+senha, Google e link mágico, com recuperação de senha e confirmação de e-mail.

## Decisão

O front autentica direto no Supabase Auth (@supabase/ssr). A API recebe o access token como Bearer e valida assinatura, emissor, audiência e expiração via JWKS do projeto (fallback HS256 para ambiente local). O sub do token é o id do perfil.

## Consequências

Nenhuma senha ou fluxo de e-mail é implementado por nós. Revogação de sessão depende da expiração curta do access token.
