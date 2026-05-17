# Git e GitHub - MRP_LOCAL

Versao de referencia: v0.1.006
Data do registro: 2026-05-17
Status: `GIT_GITHUB_PREPARADO_DOCUMENTALMENTE`

## Estrutura oficial

- `01-mrp`: sistema implementado/aprovado.
- `02-docs`: documentacao, historico, regras e decisoes.
- `03-vs`: versionamento, patches, testes, releases e preparacao.

## Regra central

`01-mrp` nao e laboratorio.

O trabalho deve ocorrer primeiro em `03-vs`, com registro em `02-docs`. `01-mrp` so recebe arquivos depois de aprovacao e promocao formal.

## Fluxo oficial Git/GitHub

### Antes de trabalhar

```powershell
git pull --rebase
```

Objetivo: atualizar a base local antes de iniciar qualquer patch.

### Durante o trabalho

- Alterar arquivos de preparacao em `03-vs`.
- Documentar decisoes, historico, regras e progresso em `02-docs`.
- Nao usar `01-mrp` como laboratorio.
- Nao promover nada para `01-mrp` sem aprovacao formal.

### Quando aprovado

- Promover para `01-mrp` com registro em `02-docs`.
- Registrar origem, destino, motivo, status e validacao.
- Manter snapshot ou backup antes da promocao quando houver risco operacional.

### Ao concluir patch

```powershell
git add .
git commit -m "v0.1.006 - preparar git github documentalmente"
git tag v0.1.006
git push
git push --tags
```

## Papel do GitHub

O GitHub guarda historico tecnico, rastreabilidade e recuperacao, mas nao substitui `03-vs`.

`03-vs` continua sendo a area oficial de patches, testes, releases e preparacao. GitHub registra as mudancas; ele nao muda o fluxo de trabalho do projeto.

## Arquivos que nao devem ser versionados

- `node_modules/`
- `__pycache__/`
- `*.pyc`
- `.env`
- `.env.*`
- `*.log`
- `*.tmp`
- `*.bak`
- `*.db`
- `*.sqlite`
- `runtime/`
- `logs/`
- `cache/`
- `.DS_Store`
- `Thumbs.db`

## Estado desta etapa

- Preparacao Git/GitHub registrada documentalmente.
- `.gitignore` criado ou atualizado na raiz do projeto.
- `README.md` criado ou atualizado na raiz do projeto.
- `01-mrp` nao alterado.
- Backend nao criado.
- Banco nao criado.
- Frontend nao criado.
