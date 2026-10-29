# 0005. Uploads por URL assinada emitida pela API

- **Status:** Aceita
- **Data:** 2026-10-28

## Contexto

Comprovantes pertencem a uma casa; policies do Storage por casa seriam complexas e duplicariam a autorização.

## Decisão

Buckets privados. A API valida a posse e emite URLs assinadas de upload/download; o cliente comprime imagens antes de enviar.

## Consequências

A autorização fica num só lugar; exige uma ida à API antes de cada upload.
