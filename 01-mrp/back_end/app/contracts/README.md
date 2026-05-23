# Contratos internos do app

Esta pasta guarda contratos internos do backend: entrada, saida e convencoes entre camadas.

## Estado atual

- Backend FastAPI ativo em `01-mrp/back_end`.
- Produtos e o primeiro dominio backend real.
- SQLite DEV/runtime pode ser criado em `01-mrp/data/db/mrp_local_dev.sqlite`.
- Contratos devem preservar resposta consistente e erros previsiveis.

## Regra

Documentos antigos que diziam "sem FastAPI" ou "sem banco" nao sao mais fonte atual. Consultar primeiro:

- `02-docs/REGRAS_ATUAIS_MRP.txt`
- `02-docs/LOG_PROGRESSO_MRP.txt`
