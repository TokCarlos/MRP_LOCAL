# v0.1.016 - Correcao overflow Produtos (mobile)

## Cenario

Mesmo apos ajustes anteriores, a aba Produtos ainda apresentava faixa/margem branca no lado direito em mobile, indicando overflow horizontal.

## Causa identificada

- A tabela `.preview-table` estava com largura minima fixa (`36rem`) para preservar leitura.
- Em telas menores, essa largura pode ultrapassar a viewport.
- O comportamento esperado e manter essa largura dentro de um wrapper com rolagem horizontal local, sem empurrar o `body`.

## Correcao aplicada

Arquivo: `01-mrp/front_end/css/responsive.css`

1. Reforco de largura base:
   - `html { width: 100%; }`
   - `body { width: 100%; overflow-x: hidden; }`
2. Wrapper da tabela:
   - `.table-responsive { display: block; max-width: 100%; overflow-x: auto; }`
3. Tabela:
   - de `min-width: 36rem` para `width: max(100%, 36rem); min-width: 0;`
4. Ajuste para telas pequenas:
   - em `@media (max-width: 480px)`, tabela para `width: max(100%, 32rem);`

## Resultado esperado

- Em 390px/430px/360px, nao deve aparecer overflow horizontal no `body`.
- Se o conteudo da tabela exceder a largura, a rolagem deve ocorrer apenas dentro de `.table-responsive`.
