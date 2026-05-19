# Recuperação — MRP_LOCAL

## Recuperação atual

O watchdog executa healthcheck contínuo e tenta reiniciar o frontend quando falha.

Script:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_watchdog.ps1"
```

## O que precisa ser validado

- Matar processo manualmente e confirmar reinício.
- Verificar logs em `01-mrp/logs/servicos`.
- Confirmar que não há loop agressivo.
- Confirmar resposta HTTP após recuperação.
