# Execucao Automatica Frontend

Status atual: frontend estatico, sem backend FastAPI e sem PostgreSQL.

Comando manual antigo (descontinuado para operacao diaria):

```powershell
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"
```

Comando operacional novo:

```powershell
py -m http.server 8765 --bind 0.0.0.0 --directory "X:\01-mrp\front_end"
```

Execucao automatica em teste:

- Script watchdog: `X:\03-vs\scripts\servicos\mrp_frontend_watchdog.ps1`
- Tarefa Windows: `MRP_LOCAL_FRONTEND`
- Inicio no logon do usuario atual
- Sem loop infinito: maximo 10 tentativas em janela maxima de 1 minuto por execucao do watchdog.
