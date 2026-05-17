# Registro v0.1.007 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `REFATORACAO_FRONTEND_LOCAL_BASE`

## Objetivo

Preparar o front-end antigo `mrp-main` em modo local temporario, com login `admin` / `admin`, sem StackAuth, sem Neon REST e sem dependencia de hospedagem online.

## Origem

`03-vs/entrada_original/mrp-main.zip`

## Destinos

- Extracao: `03-vs/patches/v0.1.007/origem_extraida`.
- Base de trabalho: `03-vs/patches/v0.1.007/mrp_local_frontend_base`.
- Front-end refatorado: `03-vs/patches/v0.1.007/mrp_local_frontend_base/front_end`.
- Documentacao: `02-docs/docs/patch/versoes/v0.1.007`.

## Arquivos e pastas criados ou atualizados

- `03-vs/patches/v0.1.007/origem_extraida`.
- `03-vs/patches/v0.1.007/mrp_local_frontend_base`.
- `03-vs/patches/v0.1.007/mrp_local_frontend_base/front_end`.
- `03-vs/patches/v0.1.007/mrp_local_frontend_base/front_end/data/mock_data.json`.
- `03-vs/patches/v0.1.007/mrp_local_frontend_base/README_LOCAL.md`.
- `02-docs/docs/patch/versoes/v0.1.007/triagem_mrp_main.md`.
- `02-docs/docs/patch/versoes/v0.1.007/checklist.md`.
- `02-docs/docs/patch/versoes/v0.1.007/registro.md`.

## Dependencias online encontradas

- StackAuth.
- Stack project id e public key no original.
- Neon REST.
- URL externa Neon.
- URL externa StackAuth.
- Header `Authorization: Bearer`.
- Token JWT online obrigatorio.
- Dependencia pratica de hospedagem online.

## Removido ou substituido

- StackAuth substituido por autenticacao local temporaria.
- Neon REST substituido por adaptador local com dados mockados.
- JWT online substituido por sessao local em `localStorage`.
- Dependencia de dominio/hospedagem substituida por execucao via servidor estatico local.
- Helper de API online desativado em `utils.js`.

## Validacao

- Busca textual sem dependencias online em `front_end`.
- Sintaxe JS validada com Node nos arquivos principais.
- `login.html` e `index.html` respondem HTTP 200 via servidor estatico temporario.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Dependencias instaladas: NAO.
- Arquivos originais apagados: NAO.
- Promocao para `01-mrp`: NAO.

## Status de promocao

Nao pronto para promocao imediata.

Pronto para avaliacao local em `03-vs`.
