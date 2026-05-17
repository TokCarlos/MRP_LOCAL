# Registro v0.1.006 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `GIT_GITHUB_PREPARADO_DOCUMENTALMENTE`

## Objetivo

Preparar o projeto para versionamento Git/GitHub sem alterar o sistema funcional.

## Escopo

- Criar ou atualizar `.gitignore` na raiz `X:\`.
- Criar ou atualizar `README.md` na raiz `X:\`.
- Criar `02-docs/docs/geral/git_github.md`.
- Registrar o fluxo oficial Git/GitHub.
- Registrar que GitHub guarda historico, mas nao substitui `03-vs`.
- Registrar que `01-mrp` nao e laboratorio.

## Fluxo oficial registrado

### Antes de trabalhar

`git pull --rebase`

### Durante o trabalho

Alterar `03-vs` e documentar em `02-docs`.

### Quando aprovado

Promover para `01-mrp` com registro.

### Ao concluir patch

`git add`, `git commit`, `git tag`, `git push`.

## Arquivos criados ou atualizados

- `X:\.gitignore`.
- `X:\README.md`.
- `02-docs/docs/geral/git_github.md`.
- `02-docs/docs/patch/versoes/v0.1.006/registro.md`.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Frontend criado: NAO.
- Arquivos apagados: NAO.
- Sistema funcional alterado: NAO.

## Observacao

O GitHub deve ser usado para historico tecnico, rastreabilidade e recuperacao. Ele nao substitui `03-vs`, que continua sendo a area oficial de versionamento, patches, testes, releases e preparacao.
