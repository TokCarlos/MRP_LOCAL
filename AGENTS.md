# AGENTS.md â€” MRP_LOCAL

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

- Versao: v0.1.036
- Fase: frontend visual em MOCK_LOCAL / correÃ§Ã£o preventiva / sem backend real

## PROTOCOLO OBRIGATORIO DE FECHAMENTO AUTOMATICO

A partir da v0.1.014, toda tarefa concluida pelo Codex no projeto MRP_LOCAL deve terminar com fechamento automatico Git.

Regra central:

- AUTO_COMMIT_E_PUSH = padrao obrigatorio.
- FECHAMENTO_MANUAL = excecao somente quando solicitado explicitamente pelo usuario.

Fluxo oficial:

- 03-vs prepara.
- 02-docs registra.
- 01-mrp executa.
- GitHub guarda.

Regras obrigatorias:

1. Toda tarefa deve terminar com documentacao em 02-docs.
2. Toda tarefa deve ter versao.
3. Toda tarefa deve ser registrada em 02-docs/docs/patch/versoes.
4. Ao concluir, deve executar fechamento Git automatico quando houver alteracao real.
5. Se nao houver alteracao real, nao criar commit vazio.
6. Se a tag ja existir, nao recriar; informar e tentar enviar a tag existente.
7. O GitHub e o cofre de historico do projeto.
8. O Codex nao deve perguntar se deve commitar quando uma tarefa for concluida.
9. Se git pull --rebase gerar conflito, parar e avisar.

O Codex so deve evitar commit/push quando o usuario disser explicitamente:

- "nao commita"
- "nao de push"
- "vou commitar manualmente"
- "fechamento manual"
- "nao fechar versao"

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
- .codex, quando versionavel

Se encontrar arquivo proibido, parar e avisar. Nao fazer commit.

Fechamento Git automatico padrao:

```powershell
.\03-vs\scripts\git_fechar_versao.ps1 -Versao "vX.Y.Z" -Mensagem "descricao curta" -Auto
```

## Excecao ativa desta entrega

Na entrega v0.1.033, o usuario solicitou commit manual. Portanto, nao executar fechamento automatico para este pacote.


Regra de infraestrutura v0.1.036:

- Porta oficial frontend estatico: 8765
- Bind oficial: 0.0.0.0
- Tailscale para remoto, LAN como principal
- Nao usar MEGA na arquitetura
