# v0.1.021 - Solucao

## Escopo aplicado

Ajuste exclusivo da listagem de Produtos, sem alteracao visual global.

## Ordem oficial de colunas aplicada

`ID | Preview | ATA+Nº | Nº Item | Produto | Empresa | Ação`

## Regras implementadas

- `ID`: usa `id` interno global.
- `Preview`: thumbnail com fallback para placeholder.
- `ATA+Nº`: coluna calculada em JS por `arp + ata_numero`.
- `Nº Item`: usa `item_ata` como string (inclui decimais).
- `Produto`: usa `nome_oficial`, alinhado a esquerda, com quebra de texto.
- `Empresa`: usa `empresa`.
- `Ação`: botao Editar centralizado.

## Arquivos alterados

- `01-mrp/front_end/pages/produtos_list.html`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/front_end/css/pages/produtos_list.css`

## Complemento visual aplicado

- Cabecalhos da tabela em maiusculo:
  `ID | PREVIEW | ATA+Nº | Nº ITEM | PRODUTO | EMPRESA | AÇÃO`
- Fundo da tabela Produtos ajustado para branco translucido (~70%):
  `background: rgba(255, 255, 255, 0.70)`
- Cabecalho da tabela com reforco de leitura:
  `background: rgba(255, 255, 255, 0.82)`
- Texto interno da tabela em cor escura para contraste:
  `color: #111`
- Produto mantido alinhado a esquerda; demais colunas centralizadas.
- Escurecimento do fundo da pagina em ~20% sem editar imagem:
  overlay aplicado no `background` do `body` com `linear-gradient(rgba(0,0,0,0.20), ...)`.
