# Promocao Front-end Base - v0.1.008

Data do registro: 2026-05-17
Status: `FRONTEND_BASE_PROMOVIDO_PARA_01_MRP`

## Promocao registrada

O front-end base preparado em `03-vs` foi promovido para `01-mrp/front_end`.

## Origem

`03-vs/patches/v0.1.007/mrp_local_frontend_base/front_end`

## Destino

`01-mrp/front_end`

## Motivo

Executar teste oficial no sistema principal.

## Causa do erro anterior

O erro 404 ocorreu porque o servidor local apontava para uma pasta sem `login.html` ou porque o `login.html` ainda nao estava promovido para `01-mrp/front_end`.

## Resultado da promocao

A promocao disponibilizou `login.html` em `X:\01-mrp\front_end` e o front-end base passou a abrir corretamente via servidor local.

## Regras observadas nesta tarefa documental

- Nao alterar codigo funcional nesta etapa de registro.
- Nao criar backend.
- Nao criar banco.
- Nao apagar arquivos.
