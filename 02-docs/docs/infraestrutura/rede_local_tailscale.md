# Rede local e Tailscale — MRP_LOCAL

## LAN

A LAN é o acesso principal do sistema local.

Validar:

- `http://localhost:8765` na máquina servidora;
- `http://IP_DA_MAQUINA:8765` em outro PC da rede.

## Tailscale

Tailscale pode ser usado para acesso remoto seguro. Não usar exposição pública direta nesta fase.

## Regra

Tailscale é adaptador de acesso. Regra de negócio não depende dele.
