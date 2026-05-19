# Firewall — MRP_LOCAL

## Porta

Porta configurada atual: `8765`.

A porta é lida de `01-mrp/config/mrp_local.env.json`.

## Script

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_firewall_8765.ps1"
```

## Regra

Firewall liberado não significa sistema blindado. Ainda é necessário validar porta, HTTP, LAN, Tailscale, watchdog e tarefa.
