# Registro v0.1.014 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `FECHAMENTO_AUTOMATICO_PADRAO_PERSISTIDO`

## Objetivo

Persistir a regra operacional obrigatoria de fechamento automatico Git para toda tarefa concluida pelo Codex no projeto `MRP_LOCAL`.

## Regra central

- `AUTO_COMMIT_E_PUSH` = padrao obrigatorio.
- `FECHAMENTO_MANUAL` = excecao somente quando solicitado explicitamente pelo usuario.

## Arquivos criados ou atualizados

- `AGENTS.md`.
- `02-docs/docs/geral/protocolo_fechamento_tarefa.md`.
- `02-docs/docs/geral/git_github.md`.
- `02-docs/docs/patch/versoes/v0.1.014/registro.md`.
- `03-vs/scripts/git_fechar_versao.ps1`.

## Conteudo registrado em AGENTS.md

- Toda tarefa concluida pelo Codex deve terminar com fechamento automatico Git.
- O Codex nao deve perguntar se deve commitar quando uma tarefa for concluida.
- Fechamento manual so ocorre quando o usuario pedir explicitamente.
- Toda versao deve ter registro em `02-docs/docs/patch/versoes/v0.1.XXX`.
- Se nao houver alteracao real, nao criar commit vazio.
- Se houver arquivo proibido versionavel, parar e avisar.
- Se tag ja existir, nao recriar; informar e tentar enviar a tag existente.
- Se `git pull --rebase` gerar conflito, parar e avisar.

## Frases que ativam excecao manual

- `nao commita`.
- `nao de push`.
- `vou commitar manualmente`.
- `fechamento manual`.
- `nao fechar versao`.

## Fluxo oficial registrado

```text
03-vs prepara
02-docs registra
01-mrp executa
GitHub guarda
```

## Arquivos proibidos antes de commit

A validacao deve respeitar `.gitignore` e verificar somente arquivos versionaveis:

```powershell
git ls-files -o --exclude-standard
git diff --name-only
git diff --cached --name-only
```

Itens proibidos versionaveis:

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

A pasta `.codex` ignorada nao deve bloquear.

## Script atualizado

`03-vs/scripts/git_fechar_versao.ps1`

Parametros:

- `Versao`.
- `Mensagem`.
- `Auto`.

Comando automatico padrao:

```powershell
powershell -ExecutionPolicy Bypass -File "X:\03-vs\scripts\git_fechar_versao.ps1" -Versao "v0.1.014" -Mensagem "persistir fechamento automatico padrao" -Auto
```

## Ordem do script

1. `Set-Location X:\`.
2. `git status`.
3. Validar arquivos proibidos versionaveis.
4. `git add .`.
5. Verificar se ha staged changes.
6. Se nao houver staged changes: informar `Nada para commitar` e sair sem commit/tag.
7. `git commit -m "$Versao - $Mensagem"`.
8. `git pull --rebase`.
9. Se tag nao existir: `git tag $Versao`.
10. `git push`.
11. `git push origin $Versao`.
12. `git status` final.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Layout alterado: NAO.
- Apenas regra, documentacao e script: SIM.

## Fechamento desta tarefa

Por regra definida nesta tarefa, o fechamento automatico deve ser executado ao final usando:

```powershell
powershell -ExecutionPolicy Bypass -File "X:\03-vs\scripts\git_fechar_versao.ps1" -Versao "v0.1.014" -Mensagem "persistir fechamento automatico padrao" -Auto
```
