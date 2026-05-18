# IA e MCP no MRP_LOCAL

MCP sera usado como camada auxiliar para IA/Codex.

Finalidade:

- consultar documentacao
- apoiar auditoria
- apoiar inventario
- apoiar versionamento
- ajudar no desenvolvimento controlado

MCP nao faz parte do sistema usado pelos funcionarios.

O sistema principal continua sendo:

Usuario -> Navegador -> Front-end -> FastAPI -> PostgreSQL -> Arquivos fisicos

Nesta fase, o MCP fica limitado a:

- X:/02-docs
- X:/03-vs

A pasta X:/01-mrp nao fica liberada para MCP nesta fase.

Status: MCP_CONFIGURADO_PARA_APOIO_DOCUMENTAL
Versao: v0.1.003
