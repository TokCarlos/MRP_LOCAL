# Registro v0.1.014 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `PROTOCOLO_FECHAMENTO_TAREFA_PERSISTIDO`

## Objetivo

Persistir o protocolo obrigatorio de fechamento de tarefa para que o Codex sempre documente, verifique arquivos indevidos, prepare commit versionado, crie tag e envie para GitHub quando uma tarefa do projeto `MRP_LOCAL` for concluida.

## Arquivos criados ou atualizados

- `AGENTS.md`.
- `02-docs/docs/geral/protocolo_fechamento_tarefa.md`.
- `02-docs/docs/geral/git_github.md`.
- `02-docs/docs/patch/versoes/v0.1.014/registro.md`.
- `03-vs/scripts/git_fechar_versao.ps1`.

## Regra registrada

Toda tarefa deve terminar com:

1. Documentacao em `02-docs`.
2. Versao propria.
3. Registro em `02-docs/docs/patch/versoes`.
4. Verificacao de arquivos proibidos.
5. Fechamento Git quando houver alteracao real.

## Fluxo oficial registrado

```text
03-vs prepara
02-docs registra
01-mrp executa
GitHub guarda
```

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

## Script criado

`03-vs/scripts/git_fechar_versao.ps1`

Parametros:

- `Versao`.
- `Mensagem`.

Comando padrao:

```powershell
.\03-vs\scripts\git_fechar_versao.ps1 -Versao "vX.Y.Z" -Mensagem "descricao curta"
```

## Comportamento do script

- Executa `Set-Location X:\`.
- Executa `git status`.
- Executa `git pull --rebase`.
- Verifica arquivos proibidos.
- Para se encontrar arquivo proibido.
- Nao cria commit vazio.
- Executa `git add .`.
- Executa `git commit -m "$Versao - $Mensagem"`.
- Cria tag se ela ainda nao existir.
- Nao recria tag existente.
- Executa `git push`.
- Executa `git push origin $Versao` quando a tag for criada.
- Executa `git status` final.

## Observacao desta tarefa

Commit nao foi executado automaticamente nesta tarefa, conforme solicitado pelo usuario.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Layout alterado: NAO.
- Apenas regra, documentacao e script: SIM.
