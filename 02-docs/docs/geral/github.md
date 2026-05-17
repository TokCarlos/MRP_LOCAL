# GitHub - MRP_LOCAL

Versao de referencia: v0.1.004
Data do registro: 2026-05-17

## Regra de repositorio

O repositorio Git deve ficar na raiz `X:\`.

O GitHub deve versionar a estrutura oficial do projeto:

- `01-mrp`
- `02-docs`
- `03-vs`

## Finalidade

O GitHub sera usado para:

- historico tecnico;
- rastreabilidade;
- recuperacao;
- auditoria de mudancas;
- comparacao entre estados do projeto.

## O que nao versionar

Nao versionar:

- arquivos temporarios;
- logs pesados;
- bancos reais;
- credenciais;
- arquivos `.env`;
- caches;
- `node_modules`;
- `__pycache__`;
- arquivos pessoais;
- runtime local.

## Releases e pacotes

Releases e pacotes podem ser guardados em `03-vs/releases`.

Arquivos grandes devem ser avaliados antes de entrar no repositorio. Quando o arquivo for pesado, sensivel ou facilmente regeneravel, registrar a decisao em `02-docs` antes de versionar.

## Relacao com fluxo de promocao

O GitHub registra o historico tecnico, mas nao substitui a regra de promocao.

`01-mrp` continua sendo area de sistema implementado. Desenvolvimento, teste e preparacao devem ocorrer primeiro em `03-vs`, com registro em `02-docs`, antes de qualquer promocao aprovada para `01-mrp`.
