# Registro v0.1.008 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `FRONTEND_BASE_PROMOVIDO_PARA_01_MRP`

## Objetivo

Registrar a promocao do front-end base para `01-mrp/front_end` para permitir teste oficial no sistema principal.

## Origem

`03-vs/patches/v0.1.007/mrp_local_frontend_base/front_end`

## Destino

`01-mrp/front_end`

## Motivo

Executar teste oficial no sistema principal.

## Contexto

O erro 404 anterior foi resolvido porque `login.html` nao existia em `X:\01-mrp\front_end` ou ainda nao havia sido promovido para `01-mrp`.

Apos a promocao do front-end base de `03-vs` para `01-mrp/front_end`, a pagina passou a abrir corretamente via servidor local.

## Teste registrado

- Pasta: `X:\01-mrp\front_end`.
- Comando: `py -m http.server 8000 --bind 0.0.0.0`.
- URL local: `http://localhost:8000/login.html`.
- Resultado: pagina abriu corretamente.

## Controle de escopo

- Codigo funcional alterado nesta tarefa documental: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Arquivos apagados: NAO.

## Arquivos documentais desta versao

- `02-docs/docs/patch/versoes/v0.1.008/registro.md`.
- `02-docs/docs/patch/versoes/v0.1.008/promocao.md`.
- `02-docs/docs/patch/versoes/v0.1.008/teste_web.md`.
