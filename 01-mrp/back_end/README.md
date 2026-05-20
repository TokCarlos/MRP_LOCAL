# back_end

Direcao futura: backend FastAPI local/rede para o MRP_LOCAL.

Estado atual:
- backend ainda nao e operacional;
- frontend atual ainda nao depende de backend;
- v0.1.045 nao cria API funcional;
- v0.1.051 cria base tecnica e contrato do modulo Produtos sem ativar servidor.

Regras:
- nao implementar endpoints reais nesta etapa;
- nao criar banco real nesta etapa;
- concentrar validacao e persistencia na API futura, nao no frontend;
- usar configuracao de ambiente e evitar caminho fisico fixo como regra de negocio.

v0.1.051:

- primeiro dominio real do backend: Produtos;
- seed atual segue como fonte temporaria de leitura;
- sem FastAPI ativo, sem banco real e sem instalacao de dependencias.
