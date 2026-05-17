# Registro v0.1.005 - MRP_LOCAL

Data do registro: 2026-05-17

## Status

`REFATORACAO_FRONTEND_LOCAL_BASE`

## Escopo

Triagem e refatoracao inicial do `mrp-main` para base front-end local temporaria do `MRP_LOCAL`.

## Origem

`03-vs/entrada_original/mrp-main.zip`

## Destinos

- Extracao: `03-vs/patches/v0.1.005/origem_extraida`.
- Base de trabalho: `03-vs/patches/v0.1.005/mrp_local_frontend_base`.
- Documentacao: `02-docs/docs/patch/versoes/v0.1.005`.

## Alteracoes realizadas

- Extraido `mrp-main.zip` em area de patch.
- Copiado `front_end` para base local de trabalho.
- Refatorado login para modo local temporario `admin` / `admin`.
- Refatorado adaptador de API para dados mockados locais.
- Refatorada seguranca para sessao local temporaria.
- Criado `front_end/data/mock_data.json`.
- Criado `README_LOCAL.md`.
- Criada documentacao de triagem, checklist e registro da versao.
- Validada resposta HTTP local de `login.html` e `index.html` com servidor estatico temporario.

## Dependencias removidas

- StackAuth.
- Neon REST.
- URLs externas de API.
- Token JWT online obrigatorio.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Dependencias instaladas: NAO.
- Arquivos originais apagados: NAO.
- Promocao para `01-mrp`: NAO.
