# Modulo Produtos - Modelo de dados (v0.1.020)

## Arquivo base

- `01-mrp/front_end/data/produtos_seed.json`

## Campos do produto

- `id` (numero): identificador interno global sequencial.
- `produto_key` (string): chave unica tecnica por `EMPRESA + ARP + ATA + ITEM`.
- `empresa` (string): valor oficial de exibicao.
- `empresa_key` (string): chave tecnica normalizada.
- `arp` (string): valor oficial de exibicao.
- `arp_key` (string): chave tecnica normalizada.
- `ata_numero` (string): valor oficial de exibicao.
- `ata_key` (string): chave tecnica normalizada.
- `item_ata` (string): item oficial da ata, preservado como string.
- `item_key` (string): chave tecnica normalizada do item.
- `nome_oficial` (string): nome oficial exatamente como entrada.
- `categoria` (string): provisoria por inferencia textual (`ATI`, `PLAYGROUND`, `MOBILIARIO`, `PENDENTE_CLASSIFICACAO`).
- `imagem` (objeto):
  - `pasta`
  - `preview`
  - `status` (`DEMO`)
- `status` (string): `ATIVO`.

## Regras

- `item_ata` nao e `id`.
- `id` e interno e pode mudar em nova carga.
- exibicao usa `nome_oficial`; chaves tecnicas sao para roteamento/arquivos.
