# Modulo Produtos - Modelo logico inicial (v0.1.051)

## Estruturas logicas

### empresas

- `id`
- `key`
- `nome_visual`
- `ativo`

### atas

- `id`
- `key`
- `nome_canonico`
- `numero_ata`
- `empresa_key` (ou `empresa_id`)
- `ativo`

### categorias

- `id`
- `key`
- `nome_visual`
- `ativo`

### produtos

- `id`
- `produto_key`
- `empresa_key` (ou `empresa_id`)
- `ata_key` (ou `ata_id`)
- `categoria_key` (ou `categoria_id`)
- `item_ata`
- `nome_oficial`
- `nome_busca`
- `imagem_path`
- `ativo`
- `created_at`
- `updated_at`

## Regras de modelagem

- `produto_key` deve ser unico.
- `item_ata` e chave de negocio contextual por empresa+ata.
- `imagem_path` pode ficar na tabela de produtos na primeira fase.
- Tabela `produto_imagens` sera criada apenas se houver necessidade real de multiplas imagens por produto.
- Visual pode usar acento; campos tecnicos devem ser ASCII-safe quando forem keys.

## Fonte atual e transicao

- seed atual: `01-mrp/front_end/data/produtos_seed.json` (temporario/mock).
- fonte real futura: PostgreSQL.
- adapter backend da v0.1.051 tolera variacoes de campo do seed sem reescrever o seed.
