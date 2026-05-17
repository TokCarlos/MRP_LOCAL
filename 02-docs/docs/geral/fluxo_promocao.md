# Fluxo de Promocao - MRP_LOCAL

Versao de referencia: v0.1.004
Data do registro: 2026-05-17

## Estrutura oficial

- `03-vs`: area de desenvolvimento, teste e preparacao.
- `02-docs`: area de registro, regra, validacao, historico, decisoes, progresso e auditoria.
- `01-mrp`: area de sistema implementado e estado atual em uso.

## Regra central

`01-mrp` nunca e laboratorio.

`01-mrp` so recebe arquivos aprovados. O Codex deve trabalhar primeiro em `03-vs`, documentar em `02-docs` e so alterar `01-mrp` quando houver tarefa explicita de promocao aprovada.

## Promocao de alteracoes

Alteracoes aprovadas devem ser promovidas para `01-mrp`, nao movidas de forma improvisada.

Antes de qualquer promocao para `01-mrp`, deve existir snapshot ou backup suficiente para recuperacao do estado anterior.

Fluxo recomendado:

1. Preparar ou testar a mudanca em `03-vs`.
2. Registrar regra, decisao, checklist ou evidencia em `02-docs`.
3. Validar escopo, risco e estado esperado.
4. Criar snapshot ou backup antes da promocao.
5. Promover para `01-mrp` somente com aprovacao explicita.
6. Registrar resultado da promocao e estado final em `02-docs`.

## Status possiveis

- `RASCUNHO`: item registrado, ainda sem teste ou validacao.
- `EM_TESTE`: item em teste ou preparacao em `03-vs`.
- `APROVADO`: item validado e autorizado para promocao futura.
- `PROMOVIDO_PARA_01`: item promovido para `01-mrp`.
- `HOMOLOGADO`: item conferido no sistema implementado.
- `REJEITADO`: item recusado, arquivado ou mantido fora do sistema.

## Estado atual registrado

- `X:\` existe e aponta para `\\HOME-MACHINE\system_jpl`.
- Pastas oficiais existentes: `01-mrp`, `02-docs`, `03-vs`.
- MCP `mrp_docs_fs` ativo.
- MCP liberado somente para `02-docs` e `03-vs`.
- `01-mrp` bloqueado no MCP nesta fase.
- Codex App instalado e funcional.
- Backend nao iniciado.
- Banco nao iniciado.
- Frontend nao iniciado.
- Sistema funcional ainda nao implementado.
