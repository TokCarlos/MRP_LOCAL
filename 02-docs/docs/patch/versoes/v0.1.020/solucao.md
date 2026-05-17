# v0.1.020 - Solucao

## Importacao oficial

- Fonte: bloco TSV oficial enviado pelo usuario no prompt da versao.
- Resultado: `147` produtos em `01-mrp/front_end/data/produtos_seed.json`.
- `nome_oficial` preservado exatamente como na entrada.
- `item_ata` preservado como string (incluindo valores decimais como `1.1`, `2.7`, `6.1`).
- `id` definido como sequencial interno global.

## Estrutura de imagem demo

- Placeholder: `01-mrp/front_end/assets/produtos/_placeholder.svg`
- Preview por item:
  `01-mrp/front_end/assets/produtos/{empresa_key}/{arp_key}/{ata_key}/{item_key}/preview.svg`
- Imagens sao demo locais e serao substituidas por imagens reais posteriormente, ATA por ATA.

## Produtos na tela

- `pages/produtos_list.html` e `js/pages/produtos_list.js` atualizados para carregar o seed local e exibir thumbnail demo por item.
- Fallback para placeholder se preview falhar.
- Correcao mobile de Produtos preservada (sem mudanca de CSS responsivo desta etapa).

## Normalizacao tecnica aplicada

- Chaves tecnicas para `empresa_key`, `arp_key`, `ata_key`, `item_key`.
- `produto_key` por combinacao de `empresa + arp + ata + item`.
- Categoria provisoria inferida por regra textual (`ATI`, `PLAYGROUND`, `MOBILIARIO`, `PENDENTE_CLASSIFICACAO`).
