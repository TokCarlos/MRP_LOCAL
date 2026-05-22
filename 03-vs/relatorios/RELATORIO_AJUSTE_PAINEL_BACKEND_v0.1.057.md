# RELATORIO_AJUSTE_PAINEL_BACKEND_v0.1.057

Data: 2026-05-22
Escopo: ajuste do painel local DEV para controle do backend, correcao de scroll e Enter. Sem commit.

## Auditoria rapida antes da alteracao

1. Inicio frontend:
   - painel chamava `mrp_frontend_start.ps1` via `run_service()`.
   - execucao ja era feita em thread por `queue_action()`.
2. Parada frontend:
   - painel chamava `mrp_frontend_stop.ps1`.
3. Status frontend:
   - painel chamava `mrp_frontend_status.ps1` em acao de usuario.
4. Healthcheck frontend:
   - painel chamava `mrp_frontend_healthcheck.ps1` em acao de usuario.
5. Backend:
   - existiam scripts backend em `03-vs/scripts/servicos`, mas o painel nao tinha botoes/acoes para backend.
6. Logs/console:
   - logs eram impressos em `ScrolledText`, com `append()` e `see(END)`.
7. Scroll:
   - area de logs tinha rolagem propria.
   - area principal de cards/botoes nao estava dentro de `Canvas` com `Scrollbar`, entao a barra geral nao existia/nao funcionava quando a janela ficava pequena.
8. Enter:
   - nao havia bind central para `<Return>` ou `<KP_Enter>` no painel.
   - dialogo admin tambem nao confirmava pelo Enter.
9. Botoes durante processo:
   - `busy` ja desabilitava botoes durante execucao.
10. Subprocessos:
   - `queue_action()` ja usava thread daemon; a UI nao deveria bloquear durante start/stop/status/healthcheck.

## Correcoes aplicadas

### Painel local DEV

- Incluidos status visual e porta do backend:
  - `Porta 8876`
  - `Backend`
- Incluidas acoes de usuario:
  - `Status Backend`
  - `Healthcheck Backend`
- Incluidas acoes administrativas:
  - `Iniciar Backend`
  - `Parar Backend`
  - `Reiniciar Backend`
- Mantida execucao assincrona via thread e `subprocess.run()`.
- Mantido console interno do painel para exibicao de saida dos scripts.

### Scroll

- Area principal do painel foi colocada em `Canvas` com `Scrollbar` vertical.
- `scrollregion` passa a ser atualizada em `<Configure>`.
- Largura do frame interno acompanha o canvas.
- Mouse wheel no Windows passa a rolar a area principal quando o foco nao estiver no console.
- Console de logs continua com rolagem propria.

### Enter

- Painel passa a tratar `<Return>` e `<KP_Enter>`.
- Se o foco estiver em botao, Enter aciona o botao.
- Se houver processo em execucao (`busy=True`), Enter e bloqueado para evitar comando duplicado.
- Dialogo de login admin confirma com Enter e cancela com Escape.

## Scripts backend criados/ajustados

### `03-vs/scripts/servicos/mrp_backend_start.ps1`

- Prioriza `01-mrp/runtime/venv_backend/Scripts/python.exe`.
- Depois tenta `python` do PATH e `py` launcher.
- Valida imports `fastapi`, `uvicorn`, `pydantic`.
- Mostra aviso claro quando `venv_backend` estiver ausente.
- Se dependencias faltarem, orienta:
  - `03-vs/scripts/backend/setup_backend_dev_env.ps1`
- Usa:
  - `python -m uvicorn app.main:app --host 0.0.0.0 --port 8876 --app-dir 01-mrp/back_end`

### `03-vs/scripts/servicos/mrp_backend_stop.ps1`

- Verifica processos em LISTEN na porta `8876`.
- Encerra somente o processo dono da porta `8876`.
- Nao mata Python generico sem validar porta.
- Retorna mensagem clara quando a porta ja esta livre.

### `03-vs/scripts/servicos/mrp_backend_status.ps1`

- Verifica porta `8876`.
- Lista PIDs donos da porta e linha de comando do processo.
- Testa:
  - `/health`
  - `/api/status`
- Retorna exit code coerente.

### `03-vs/scripts/servicos/mrp_backend_healthcheck.ps1`

- Testa:
  - `/health`
  - `/api/status`
  - `/api/produtos`
  - `/api/produtos/bases`
- Usa timeout curto.
- Exibe resultado individual por endpoint.

## Arquivos alterados/criados

- `03-vs/scripts/painel/mrp_painel_controle.py`
- `03-vs/scripts/servicos/mrp_backend_start.ps1`
- `03-vs/scripts/servicos/mrp_backend_stop.ps1`
- `03-vs/scripts/servicos/mrp_backend_status.ps1`
- `03-vs/scripts/servicos/mrp_backend_healthcheck.ps1`
- `03-vs/relatorios/RELATORIO_AJUSTE_PAINEL_BACKEND_v0.1.057.md`
- `03-vs/relatorios/RELATORIO_BACKEND_PRODUTOS_v0.1.057.md`
- `02-docs/docs/geral/status_geral.md`

## Pendencias

- Testar manualmente o painel em janela reduzida.
- Testar rolagem com mouse wheel e barra lateral.
- Testar Enter com foco em cada botao.
- Testar start/stop/status/healthcheck pelo painel aberto.
- Nao considerar painel homologado/blindado.

## Validacoes executadas

- `python -m py_compile 03-vs/scripts/painel/mrp_painel_controle.py`: OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File 03-vs/scripts/servicos/mrp_backend_start.ps1`: OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File 03-vs/scripts/servicos/mrp_backend_status.ps1`: OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File 03-vs/scripts/servicos/mrp_backend_healthcheck.ps1`: OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File 03-vs/scripts/servicos/mrp_backend_stop.ps1`: OK.
- `git diff --check`: OK.
- Cache gerado por `py_compile` removido: `03-vs/scripts/painel/__pycache__`.
