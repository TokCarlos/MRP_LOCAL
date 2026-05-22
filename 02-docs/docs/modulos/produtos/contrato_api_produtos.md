# Contrato API Produtos (planejado) - v0.1.051

## Endpoints planejados para primeira fase de leitura

- `GET /api/health`
- `GET /api/version`
- `GET /api/produtos`
- `GET /api/produtos/{produto_key}`
- `GET /api/empresas`
- `GET /api/atas`
- `GET /api/categorias`

## Endpoints futuros fora de escopo agora

- `POST /api/produtos`
- `PUT /api/produtos/{produto_key}`
- `POST /api/atas`
- `POST /api/produtos/{produto_key}/imagem`
- vinculo de materiais/BOM por produto

## Observacoes

- Este contrato e planejado, sem API ativa nesta etapa.
- FastAPI, SQLAlchemy e PostgreSQL ficam para ativacao futura.
- Fonte atual permanece o seed local, via adapter interno.
- Chaves tecnicas devem ser ASCII-safe; texto visual pode manter acentos corretos.

## Atualizacao v0.1.058

- `GET /api/produtos` deve retornar lista em `{ ok: true, data: [...] }`.
- Cada item de lista deve trazer os campos essenciais usados pelo frontend: `id`, `produto_key`, `base_ata_id`, `item_ata`, `nome_oficial`, `categoria`, `imagem_path`, `imagem.preview`, `ativo`, `ata_key`, `ata_numero`, `arp`, `empresa_key` e `empresa`.
- `GET /api/produtos/{id}` deve manter o mesmo contrato essencial da listagem.
- `POST /api/produtos/{id}/imagem/upload` recebe `multipart/form-data` com campo `arquivo`.
- Upload de imagem permitido: `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`.
- Limite inicial: 5 MB.
- O banco guarda caminho relativo em `produtos.imagem_path`.
- No DEV atual, upload salva em caminho publico do frontend: `assets/images/produtos/...`.
