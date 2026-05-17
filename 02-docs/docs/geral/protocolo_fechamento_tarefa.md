# Protocolo Obrigatorio de Fechamento de Tarefa - MRP_LOCAL

Versao de referencia: v0.1.014
Data do registro: 2026-05-17
Status: `PROTOCOLO_FECHAMENTO_TAREFA_PERSISTIDO`

## Objetivo

Persistir o protocolo obrigatorio que o Codex deve seguir ao concluir tarefas do projeto `MRP_LOCAL`.

## Fluxo oficial

```text
03-vs prepara
02-docs registra
01-mrp executa
GitHub guarda
```

## Regras obrigatorias

- Toda tarefa deve terminar com documentacao em `02-docs`.
- Toda tarefa deve ter versao.
- Toda tarefa deve ser registrada em `02-docs/docs/patch/versoes`.
- Ao concluir, deve executar fechamento Git quando houver alteracao real.
- Se nao houver alteracao real, nao criar commit vazio.
- Se a tag ja existir, nao recriar; apenas informar.
- O GitHub e o cofre de historico do projeto.

## Protocolo de encerramento

1. Documentar a alteracao em `02-docs`.
2. Verificar arquivos indevidos antes de versionar.
3. Executar `git status`.
4. Executar `git pull --rebase`.
5. Executar `git add .`.
6. Executar `git commit -m "<Versao> - <Mensagem>"` somente se houver alteracao real.
7. Criar tag da versao, se ainda nao existir.
8. Enviar commit para GitHub.
9. Enviar tag para GitHub.
10. Executar `git status` final.

## Arquivos proibidos antes de commit

Se qualquer item proibido for encontrado, parar e avisar. Nao fazer commit.

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
- `.codex`

## Script oficial

Script:

```text
03-vs/scripts/git_fechar_versao.ps1
```

Comando padrao:

```powershell
.\03-vs\scripts\git_fechar_versao.ps1 -Versao "vX.Y.Z" -Mensagem "descricao curta"
```

## Observacoes

- O script nao substitui a revisao tecnica do Codex.
- O script deve parar se encontrar arquivo proibido.
- O script nao deve criar commit vazio.
- O script deve informar se a tag ja existir.
- GitHub guarda o historico, mas nao substitui `03-vs`.

## Controle de escopo desta etapa

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Layout alterado: NAO.
- Apenas regra, documentacao e script: SIM.
