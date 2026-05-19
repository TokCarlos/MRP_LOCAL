# Execução automática — MRP_LOCAL

## Estado atual

A execução automática usa scripts em:

`03-vs/scripts/servicos`

A configuração central fica em:

`01-mrp/config/mrp_local.env.json`

## Tarefa Windows

Instalar tarefa no logon:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_task_install.ps1" -Schedule ONLOGON
```

Modo `ONSTART` existe no script, mas pode exigir permissão administrativa e validação específica.

## Watchdog

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_watchdog.ps1"
```

O watchdog é contínuo e usa healthcheck antes de reiniciar.

## Pendente

Validar em Windows real: logoff/logon, reboot, queda de energia e reinício após processo morto.
