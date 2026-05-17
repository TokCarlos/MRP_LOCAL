# Git e GitHub - MRP_LOCAL

Versao de referencia: v0.1.014
Data do registro: 2026-05-17
Status: `FECHAMENTO_AUTOMATICO_PADRAO_PERSISTIDO`

## Estrutura oficial

- `01-mrp`: sistema implementado/aprovado.
- `02-docs`: documentacao, historico, regras e decisoes.
- `03-vs`: versionamento, patches, testes, releases e preparacao.

## Fluxo oficial do projeto

```text
03-vs prepara
02-docs registra
01-mrp executa
GitHub guarda
```

GitHub e o cofre de historico tecnico, rastreabilidade e recuperacao do projeto, mas nao substitui `03-vs`.

## Fechamento automatico por padrao

Regra central:

- `AUTO_COMMIT_E_PUSH` = padrao obrigatorio.
- `FECHAMENTO_MANUAL` = excecao somente quando solicitado explicitamente pelo usuario.

O Codex nao deve perguntar se deve commitar quando uma tarefa for concluida.

## Excecoes explicitas

O Codex so deve evitar commit/push quando o usuario disser explicitamente:

- `nao commita`
- `nao de push`
- `vou commitar manualmente`
- `fechamento manual`
- `nao fechar versao`

## Antes de trabalhar

```powershell
git pull --rebase
```

Objetivo: atualizar a base local antes de iniciar qualquer patch.

## Durante o trabalho

- Alterar arquivos de preparacao em `03-vs` quando a tarefa for preparatoria.
- Documentar decisoes, historico, regras e progresso em `02-docs`.
- Nao usar `01-mrp` como laboratorio.
- Promover para `01-mrp` somente com escopo explicito e registro.

## Protocolo obrigatorio ao concluir tarefa

Toda tarefa deve terminar com:

1. Documentacao em `02-docs`.
2. Registro versionado em `02-docs/docs/patch/versoes/v0.1.XXX`.
3. Verificacao de arquivos proibidos versionaveis.
4. Fechamento Git automatico quando houver alteracao real.

Se nao houver alteracao real, nao criar commit vazio.

Se a tag ja existir, nao recriar; informar e tentar enviar a tag existente.

Se `git pull --rebase` gerar conflito, parar e avisar.

## Arquivos proibidos antes de commit

Validar somente arquivos versionaveis, respeitando `.gitignore`:

```powershell
git ls-files -o --exclude-standard
git diff --name-only
git diff --cached --name-only
```

Se encontrar item proibido versionavel, parar e avisar. Nao fazer commit.

- `.env`
- `.venv`
- `node_modules`
- `__pycache__`
- `*.db`
- `*.sqlite`
- `*.log` pesado
- arquivos temporarios
- credenciais
- `.codex`, quando versionavel

A pasta `.codex` ignorada por `.gitignore` nao deve bloquear.

## Script oficial de fechamento automatico

```powershell
.\03-vs\scripts\git_fechar_versao.ps1 -Versao "vX.Y.Z" -Mensagem "descricao curta" -Auto
```

## Ordem do script

```text
Set-Location X:\
git status
validar arquivos proibidos versionaveis
git add .
verificar staged changes
git commit -m "$Versao - $Mensagem"
git pull --rebase
git tag $Versao, se nao existir
git push
git push origin $Versao
git status final
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

- Fechamento automatico registrado como padrao.
- Fechamento manual registrado como excecao explicita.
- Script de fechamento atualizado com parametro `-Auto`.
- `01-mrp` nao alterado nesta tarefa.
- Backend nao criado.
- Banco nao criado.
- Layout nao alterado.
