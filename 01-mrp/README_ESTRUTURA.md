# Estrutura 01-mrp

Status: etapa intermediaria v0.1.054.

O objetivo estrutural e separar codigo, dominio, infraestrutura, operacao, dados, runtime, logs e temporarios.

Estrutura alvo:

```text
app/frontend
app/backend
core/domain
core/services
core/engine
infrastructure/adapters
infrastructure/persistence
infrastructure/config
operations/health
operations/install
operations/scripts
operations/tools
assets
data
runtime
logs
tmp
backups
docs_runtime
```

Compatibilidade preservada nesta etapa:

- `front_end` permanece ativo porque scripts e frontend ainda dependem desse caminho.
- `back_end` permanece ativo porque o backend FastAPI e imports Python dependem desse caminho.
- `config`, `health`, `install` e `tools` permanecem como pontos operacionais existentes.
- `adapters` e `engine` foram migrados para a estrutura nova por baixo risco.

Regra: novas migracoes devem atualizar referencias, validar scripts e registrar impacto antes de remover caminhos legados.
