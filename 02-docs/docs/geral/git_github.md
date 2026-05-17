# Git e GitHub - MRP_LOCAL

Versao de referencia: v0.1.014
Data do registro: 2026-05-17
Status: `PROTOCOLO_FECHAMENTO_TAREFA_PERSISTIDO`

## Estrutura oficial

- `01-mrp`: sistema implementado/aprovado.
- `02-docs`: documentacao, historico, regras e decisoes.
- `03-vs`: versionamento, patches, testes, releases e preparacao.

## Regra central

`01-mrp` nao e laboratorio.

O trabalho deve ocorrer primeiro em `03-vs`, com registro em `02-docs`. `01-mrp` so recebe arquivos depois de aprovacao e promocao formal.

## Fluxo oficial do projeto

```text
03-vs prepara
02-docs registra
01-mrp executa
GitHub guarda
```

GitHub e o cofre de historico tecnico, rastreabilidade e recuperacao do projeto, mas nao substitui `03-vs`.

## Antes de trabalhar

```powershell
git pull --rebase
```

Objetivo: atualizar a base local antes de iniciar qualquer patch.

## Durante o trabalho

- Alterar arquivos de preparacao em `03-vs`.
- Documentar decisoes, historico, regras e progresso em `02-docs`.
- Nao usar `01-mrp` como laboratorio.
- Nao promover nada para `01-mrp` sem aprovacao formal.

## Quando aprovado

- Promover para `01-mrp` com registro em `02-docs`.
- Registrar origem, destino, motivo, status e validacao.
- Manter snapshot ou backup antes da promocao quando houver risco operacional.

## Protocolo obrigatorio ao concluir tarefa

Toda tarefa deve terminar com:

1. Documentacao em `02-docs`.
2. Registro versionado em `02-docs/docs/patch/versoes`.
3. Verificacao de arquivos proibidos.
4. Fechamento Git, se houver alteracao real.

Se nao houver alteracao real, nao criar commit vazio.

Se a tag ja existir, nao recriar; apenas informar.

## Arquivos proibidos antes de commit

Se encontrar item proibido, parar e avisar. Nao fazer commit.

- `.env`
- `.venv`
- `node_modules`
- `__pycache__`
- `*.db`
- `*.sqlite`
- `*.log` pesado
- arquivos temporarios
- credenciais
- `.codex`

## Script oficial de fechamento

```powershell
.\03-vs\scripts\git_fechar_versao.ps1 -Versao "vX.Y.Z" -Mensagem "descricao curta"
```

O script executa:

```powershell
Set-Location X:\
git status
git pull --rebase
git add .
git commit -m "$Versao - $Mensagem"
git tag $Versao
git push
git push origin $Versao
git status
```

## O que nao versionar

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
- `.codex/`

## Estado desta etapa

- Protocolo obrigatorio de fechamento persistido.
- Script de fechamento criado em `03-vs/scripts`.
- `01-mrp` nao alterado nesta tarefa.
- Backend nao criado.
- Banco nao criado.
- Layout nao alterado.
