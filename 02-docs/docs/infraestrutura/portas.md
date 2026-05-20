# Portas Oficiais

Porta descontinuada:

- 8000

Porta oficial inicial do frontend MRP_LOCAL:

- 8765/TCP

Servidor atual:

- Frontend estatico servido por `py -m http.server`
- Sem backend API ativo nesta etapa.

Diretriz futura:

- `8765` deve continuar como porta interna/configuravel do frontend;
- acesso visual ao usuario final deve evoluir para nome amigavel/proxy (80/443), quando a infraestrutura estiver madura;
- essa camada nao altera regra de negocio e nao esta implementada nesta etapa.
