# v0.1.017 - Solucao

## Escopo aplicado

- Correcao minima apenas no CSS responsivo da tabela de Produtos.
- Sem alteracao de backend.
- Sem alteracao de logica JS.
- Sem alteracao estrutural de HTML.

## Arquivo alterado

- `01-mrp/front_end/css/responsive.css`

## Ajustes aplicados

No bloco `@media (max-width: 768px)`:

- `.table-responsive`:
  - `width: 100%`
  - `max-width: 100%`
  - `overflow-x: hidden`
- `.preview-table`:
  - `width: 100%`
  - `max-width: 100%`
  - `min-width: 0`
  - `table-layout: fixed`
- `.preview-table th, .preview-table td`:
  - `overflow-wrap: anywhere`
  - `word-break: normal`
- `.preview-table .btn-row-action`:
  - `max-width: 100%`
  - `white-space: normal`

No bloco `@media (max-width: 480px)`:

- substituido `width: max(100%, 32rem)` por:
  - `width: 100%`
  - `max-width: 100%`
  - `min-width: 0`

## Resultado tecnico esperado

- A tabela deixa de forcar largura fixa acima da viewport mobile.
- A pagina Produtos nao deve expandir horizontalmente o documento.
