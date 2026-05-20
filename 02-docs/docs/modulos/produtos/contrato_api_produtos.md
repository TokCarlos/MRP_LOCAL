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
