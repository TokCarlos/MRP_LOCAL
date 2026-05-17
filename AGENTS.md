# AGENTS.md — MRP_LOCAL

Estrutura oficial:

- 01-mrp = sistema funcional
- 02-docs = documentacao, regras, relatorios e progresso
- 03-vs = versionamento, pacotes, historico e releases

Regras obrigatorias:

1. Nao alterar 01-mrp sem escopo explicito.
2. Nao apagar arquivos.
3. Nao renomear 01-mrp, 02-docs ou 03-vs.
4. Nao usar acentos em nomes fisicos de arquivos ou pastas.
5. Registrar toda mudanca em 02-docs.
6. MCP e camada auxiliar para IA/Codex, nao dependencia obrigatoria do sistema.
7. O sistema MRP_LOCAL deve funcionar mesmo sem MCP.

Status atual:

- Versao: v0.1.003
- Fase: configuracao inicial MCP/IA

## PROTOCOLO OBRIGATORIO DE FECHAMENTO DE TAREFA

A partir da v0.1.014, toda tarefa do projeto MRP_LOCAL deve terminar com o protocolo de fechamento abaixo.

Fluxo oficial:

- 03-vs prepara.
- 02-docs registra.
- 01-mrp executa.
- GitHub guarda.

Regras obrigatorias:

1. Toda tarefa deve terminar com documentacao em 02-docs.
2. Toda tarefa deve ter versao.
3. Toda tarefa deve ser registrada em 02-docs/docs/patch/versoes.
4. Ao concluir, deve executar fechamento Git quando houver alteracao real.
5. Se nao houver alteracao real, nao criar commit vazio.
6. Se a tag ja existir, nao recriar; apenas informar.
7. O GitHub e o cofre de historico do projeto.

Antes de commitar, verificar se existem arquivos proibidos:

- .env
- .venv
- node_modules
- __pycache__
- *.db
- *.sqlite
- *.log pesado
- arquivos temporarios
- credenciais
- .codex

Se encontrar arquivo proibido, parar e avisar. Nao fazer commit.

Fechamento Git padrao:

```powershell
.\03-vs\scripts\git_fechar_versao.ps1 -Versao "vX.Y.Z" -Mensagem "descricao curta"
```
