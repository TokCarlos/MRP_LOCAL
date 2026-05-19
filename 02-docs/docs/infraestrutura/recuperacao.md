# Recuperacao Operacional

Checklist rapido:

1. Verificar status:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_status.ps1
```

2. Validar saude:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1
```

3. Iniciar manualmente:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_start.ps1
```

4. Parar manualmente:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_stop.ps1
```

5. Instalar tarefa automatica (teste):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_task_install.ps1
```
