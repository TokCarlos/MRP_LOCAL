# Protocolo Obrigatorio de Fechamento Automatico - MRP_LOCAL

Versao de referencia: v0.1.014
Data do registro: 2026-05-17
Status: `FECHAMENTO_AUTOMATICO_PADRAO_PERSISTIDO`

## Objetivo

Persistir o protocolo obrigatorio que o Codex deve seguir ao concluir tarefas do projeto `MRP_LOCAL`.

## Regra central

- `AUTO_COMMIT_E_PUSH` = padrao obrigatorio.
- `FECHAMENTO_MANUAL` = excecao somente quando solicitado explicitamente pelo usuario.

O Codex nao deve perguntar se deve commitar quando uma tarefa for concluida.

## Quando nao fechar automaticamente

O Codex so deve evitar commit/push quando o usuario disser explicitamente:

- `nao commita`
- `nao de push`
- `vou commitar manualmente`
- `fechamento manual`
- `nao fechar versao`

## Fluxo oficial

```text
03-vs prepara
02-docs registra
01-mrp executa
GitHub guarda
```

GitHub e o cofre de historico do projeto.

## Regras obrigatorias

- Toda tarefa deve terminar com documentacao em `02-docs`.
- Toda tarefa deve ter versao clara no formato `v0.1.XXX`.
- Toda tarefa deve ser registrada em `02-docs/docs/patch/versoes/v0.1.XXX`.
- Ao concluir, deve executar fechamento Git automatico quando houver alteracao real.
- Se nao houver alteracao real, nao criar commit vazio.
- Se a tag ja existir, nao recriar; informar e tentar enviar a tag existente.
- Se `git pull --rebase` gerar conflito, parar e avisar.

## Fechamento automatico inclui

1. Atualizar documentacao em `02-docs`.
2. Validar arquivos proibidos respeitando `.gitignore`.
3. Executar `git add .`.
4. Criar commit versionado.
5. Criar tag da versao.
6. Executar `git push`.
7. Executar `git push origin <versao>`.
8. Executar `git status` final.

## Arquivos proibidos antes de commit

Validar somente arquivos versionaveis:

```powershell
git ls-files -o --exclude-standard
git diff --name-only
git diff --cached --name-only
```

Se qualquer item proibido versionavel for encontrado, parar e avisar. Nao fazer commit.

Itens proibidos:

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

A pasta `.codex` ignorada por `.gitignore` nao deve bloquear o fechamento.

## Script oficial

Script:

```text
03-vs/scripts/git_fechar_versao.ps1
```

Comando padrao automatico:

```powershell
.\03-vs\scripts\git_fechar_versao.ps1 -Versao "vX.Y.Z" -Mensagem "descricao curta" -Auto
```

## Ordem operacional do script

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

## Controle de escopo desta etapa

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Layout alterado: NAO.
- Apenas regra, documentacao e script: SIM.
