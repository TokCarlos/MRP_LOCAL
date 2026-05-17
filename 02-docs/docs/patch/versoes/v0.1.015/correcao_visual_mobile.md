# Correcao Visual Mobile - v0.1.015B

Data do registro: 2026-05-17
Status: `LAYOUT_MOBILE_CORRECAO_CIRURGICA_APLICADA`

## Base da correcao

Relatorio usado:

`02-docs/docs/patch/versoes/v0.1.015/auditoria_visual_mobile.md`

## Snapshot antes da alteracao

Snapshot criado com sucesso em:

`03-vs/snapshots/antes_v0.1.015B/01-mrp`

## Escopo aplicado

Ajustes cirurgicos aplicados somente em:

- `01-mrp/front_end/css/responsive.css`
- `01-mrp/front_end/css/style.css`
- `01-mrp/front_end/js/pages/produtos_list.js`

Sem alteracao em:

- backend
- banco
- login/admin
- `api.js`
- `auth.js`
- `config.js`
- framework
- identidade visual

## Correcao 1 - menu mobile sem empurrar main

Problema anterior:

- `body.menu-open main` usava `margin-top` fixo grande (`240px` e `350px`).

Correcao aplicada:

- Removidas regras fixas de `body.menu-open main`.
- Menu mobile passou para modo overlay/absolute abaixo do header.
- Conteudo principal nao e mais empurrado por margem fixa no estado aberto.

## Correcao 2 - botoes Editar grandes demais

Problema anterior:

- Regra global de toque incluia `preview-table button` com `min-height: 44px`.

Correcao aplicada:

- `preview-table button` removido da regra global de `44px`.
- Criada classe `.btn-row-action` para botao de linha.
- Botao `Editar` passou a usar `.btn-row-action`.

## Correcao 3 - logo JPL colado ao titulo

Problema anterior:

- Espacamento entre logo e titulo variava por regras concorrentes.

Correcao aplicada:

- Unificado espacamento com `margin-right: clamp(8px, 1.8vw, 14px)` em `.logo-area img`.

## Correcao 4 - conflito main/header em mobile

Problema anterior:

- `style.css` e `responsive.css` definiam espacamentos concorrentes para `main` em mobile.

Correcao aplicada:

- Removido bloco mobile de `main` em `style.css` que forçava `margin-top: 120px`.
- Mantido controle de espacamento no `responsive.css` para reduzir conflito.

## Verificacao tecnica

- `node --check` aprovado para `js/pages/produtos_list.js`.
- HTTP 200 para `login.html`, `index.html` e `css/responsive.css` em servidor temporario local.
- Regra de `body.menu-open main` com margem fixa nao existe mais.

## Resultado

A correcao cirurgica foi aplicada no `01-mrp/front_end` com foco em mobile e zoom, preservando o visual geral e sem redesenho completo.
