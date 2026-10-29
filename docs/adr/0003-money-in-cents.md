# 0003. Dinheiro em centavos inteiros

- **Status:** Aceita
- **Data:** 2026-10-28

## Contexto

O sistema antigo usava float/DECIMAL e formatava valores em vários lugares.

## Decisão

Todo valor monetário é BIGINT em centavos (*_cents). A formatação BRL acontece só na borda (UI). Divisões (parcelas) distribuem o resto na primeira parcela.

## Consequências

Sem erros de arredondamento; a UI precisa converter na entrada (teclado em centavos).
