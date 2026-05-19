# v0.1.017 - Problemas

## Problema

Overflow horizontal mobile na pagina Produtos, com faixa branca lateral a direita ao arrastar.

## Causa

Arquivo: `01-mrp/front_end/css/responsive.css`  
Seletor: `.preview-table`

Regras anteriores que forcaram largura maior que viewport mobile:
- `width: max(100%, 36rem);`
- `@media (max-width: 480px) { .preview-table { width: max(100%, 32rem); } }`

Em 360px/390px/430px, a largura minima em `rem` excede a viewport.
