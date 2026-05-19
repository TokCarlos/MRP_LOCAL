# Acesso local e Tailscale — MRP_LOCAL

## Estado atual

O frontend estático usa a porta configurada em `01-mrp/config/mrp_local.env.json`, atualmente `8765`.

A raiz do projeto deve ser resolvida automaticamente pelos scripts ou informada por `MRP_LOCAL_ROOT`. Não usar caminho físico fixo como regra de negócio.

## Acesso local

1. Iniciar o frontend pelo script de serviço.
2. Validar `http://localhost:8765`.
3. Validar `http://IP_DA_MAQUINA:8765` em outro computador da LAN.

## Acesso remoto seguro

Tailscale pode ser usado como camada segura para acesso remoto. O sistema não deve ser exposto diretamente à internet nesta fase.

## Comandos

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_status.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_start.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1"
```
