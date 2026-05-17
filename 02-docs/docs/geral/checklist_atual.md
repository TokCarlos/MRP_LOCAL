# Checklist Atual - MRP_LOCAL

Versao de referencia: v0.1.004
Data do registro: 2026-05-17

## Estrutura local

- [x] `X:\` existe e aponta para `\\HOME-MACHINE\system_jpl`.
- [x] Pastas oficiais registradas: `01-mrp`, `02-docs`, `03-vs`.
- [x] `01-mrp` definido como sistema implementado / estado atual em uso.
- [x] `02-docs` definido como documentacao, regras, historico, decisoes, progresso e auditoria.
- [x] `03-vs` definido como versionamento, patches, testes, releases, snapshots e preparacao antes de promover ao sistema.

## MCP

- [x] MCP `mrp_docs_fs` ativo.
- [x] MCP liberado somente para `02-docs` e `03-vs`.
- [x] `01-mrp` bloqueado no MCP nesta fase.
- [x] MCP registrado como camada auxiliar para IA/Codex, nao dependencia obrigatoria do sistema.

## Codex

- [x] Codex App instalado e funcional.
- [x] Codex orientado a trabalhar primeiro em `03-vs` quando houver desenvolvimento ou preparacao.
- [x] Codex orientado a documentar em `02-docs`.
- [x] Codex proibido de alterar `01-mrp` sem tarefa explicita de promocao aprovada.

## Documentacao

- [x] Regra de promocao documentada.
- [x] Preparacao GitHub documentada.
- [x] Checklist atual criado.
- [x] Registro v0.1.004 criado.

## Versionamento

- [x] `03-vs` definido como area de versionamento, patches, testes, releases e snapshots.
- [x] Promocao para `01-mrp` condicionada a snapshot ou backup previo.
- [ ] Criar ou revisar politica `.gitignore`.
- [ ] Criar snapshot inicial antes de qualquer promocao futura para `01-mrp`.

## GitHub

- [x] Repositorio Git definido para a raiz `X:\`.
- [x] GitHub definido para versionar `01-mrp`, `02-docs` e `03-vs`.
- [x] Itens proibidos de versionamento registrados.
- [x] Uso do GitHub registrado para historico tecnico, rastreabilidade e recuperacao.
- [ ] Inicializar ou validar repositorio Git na raiz `X:\`.
- [ ] Validar tamanho e sensibilidade de releases/pacotes antes de versionar.

## Sistema funcional

- [x] Backend nao iniciado.
- [x] Banco nao iniciado.
- [x] Frontend nao iniciado.
- [x] Sistema funcional ainda nao implementado.
- [x] `01-mrp` nao alterado nesta tarefa.

## Proximos passos

- [ ] Revisar politica de `.gitignore` para o projeto.
- [ ] Inventariar conteudo atual de `01-mrp`, `02-docs` e `03-vs` antes do primeiro commit tecnico.
- [ ] Definir criterio de snapshot/backup antes de promocao para `01-mrp`.
- [ ] Criar rotina de registro de mudancas em `02-docs` para cada versao.
