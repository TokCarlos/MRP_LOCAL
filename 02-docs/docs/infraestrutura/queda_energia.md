# Queda de Energia e Reinicio

Risco atual:

- Sem execucao automatica, o frontend para quando o terminal fecha, maquina reinicia ou falta energia.

Mitigacao aplicada no patch v0.1.036:

- Watchdog em PowerShell.
- Tarefa agendada `MRP_LOCAL_FRONTEND` no logon.

Observacao:

- Em ambiente de teste com unidade mapeada `X:\`, a tarefa depende do contexto do usuario logado.
- Em producao futura, usar caminho local de servidor para reduzir fragilidade.
