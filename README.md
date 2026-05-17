# MRP_LOCAL

Projeto local MRP_LOCAL.

## Estrutura oficial

- `01-mrp`: sistema implementado/aprovado.
- `02-docs`: documentacao, historico, regras e decisoes.
- `03-vs`: versionamento, patches, testes, releases e preparacao.

## Regra central

`01-mrp` nao e laboratorio.

O Codex deve trabalhar primeiro em `03-vs`, documentar em `02-docs` e so alterar `01-mrp` quando houver tarefa explicita de promocao aprovada.

## Fluxo Git/GitHub

Antes de trabalhar:

```powershell
git pull --rebase
```

Durante o trabalho:

- Alterar `03-vs`.
- Documentar em `02-docs`.
- Nao alterar `01-mrp` sem aprovacao de promocao.

Quando aprovado:

- Promover para `01-mrp` com registro em `02-docs`.

Ao concluir patch:

```powershell
git add .
git commit -m "mensagem do patch"
git tag vX.Y.Z
git push
git push --tags
```

## Papel do GitHub

GitHub guarda historico tecnico, rastreabilidade e recuperacao, mas nao substitui `03-vs`.

`03-vs` continua sendo a area oficial de versionamento, patches, testes, releases e preparacao antes de qualquer promocao para `01-mrp`.

## Status v0.1.006

`GIT_GITHUB_PREPARADO_DOCUMENTALMENTE`

Nesta etapa nao foram criados backend, banco ou frontend, e `01-mrp` nao foi alterado.

## Regra de dominio (v0.1.027)

- `EMPRESA` e dominio operacional interno: `JPL`, `AÇO`, `TCR`.
- `GOV. RIO` nao e empresa; deve ser tratado como `cliente/orgao/origem de ata`.
- Filtros de `EMPRESA` e `ATA/ORIGEM` devem permanecer separados.
