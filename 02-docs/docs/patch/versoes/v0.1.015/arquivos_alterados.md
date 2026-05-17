# Arquivos Alterados - v0.1.015B

Data do registro: 2026-05-17
Status: `LAYOUT_MOBILE_CORRECAO_CIRURGICA_APLICADA`

## Snapshot

- `03-vs/snapshots/antes_v0.1.015B/01-mrp`

## Arquivos alterados

- `01-mrp/front_end/css/responsive.css`
- `01-mrp/front_end/css/style.css`
- `01-mrp/front_end/js/pages/produtos_list.js`

## Mudancas por arquivo

### `01-mrp/front_end/css/responsive.css`

- Removido `preview-table button` da regra global de toque `44px`.
- Criada classe `.btn-row-action` para botoes de linha.
- Ajustado espacamento logo/titulo em `.logo-area img` com `clamp`.
- Menu mobile convertido para overlay/absolute abaixo do header.
- Removidas margens fixas de `body.menu-open main`.

### `01-mrp/front_end/css/style.css`

- Removido bloco mobile que forçava `main { margin-top: 120px; ... }`.

### `01-mrp/front_end/js/pages/produtos_list.js`

- Botao `Editar` passou a usar classe `.btn-row-action`.

## Arquivos permitidos mas nao alterados

- `01-mrp/front_end/js/responsive.js`
- `01-mrp/front_end/index.html`

## Restricoes respeitadas

- Nao redesenhar layout inteiro.
- Nao trocar identidade visual.
- Nao instalar dependencias.
- Nao criar backend.
- Nao criar banco.
- Nao alterar login/admin.
- Nao alterar `api.js/auth.js/config.js`.
