# v0.1.022 - Solucao

## Escopo

- Ajuste somente da pagina Produtos.
- Desktop mantido em formato tabela normal.
- Mobile convertido para cards compactos por linha.

## Implementacao

Arquivos alterados:
- `01-mrp/front_end/css/pages/produtos_list.css`
- `01-mrp/front_end/js/pages/produtos_list.js`

### Desktop
- Mantida a tabela com colunas:
  `ID | PREVIEW | ATA+Nº | Nº ITEM | PRODUTO | EMPRESA | AÇÃO`
- Sem alteracao de estrutura funcional global.

### Mobile (<=768px)
- `thead` ocultado.
- `tbody` virou grid de cards.
- Cada `tr` virou card com grid interno:
  - preview a esquerda
  - produto principal (max 3 linhas)
  - ata+numero (max 2 linhas)
  - item/id/empresa em metadados compactos
  - acao com botao Editar sem quebra
- Removido comportamento de quebra letra por letra no mobile.

### Ajuste JS
- Padronizada classe da coluna de item para `col-item`.
- Mantida estrutura de dados e seed sem alteracoes.
