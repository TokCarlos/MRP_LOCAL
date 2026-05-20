# Nome amigavel e proxy futuro - v0.1.050

## Objetivo

Ocultar IP e porta na experiencia do usuario final, mantendo o MRP local-first.

Hoje: `http://IP:8765/index.html`
Futuro: nome amigavel (ex.: `http://mrp.local`, `https://mrp.local`, `https://mrp-trabalho.<tailnet>.ts.net`).

## LAN (futuro)

- hosts local nos clientes (curto prazo);
- DNS interno (medio prazo);
- nome interno (`mrp.local` / `mrp.empresa.local`);
- proxy reverso local em 80/443 encaminhando para `127.0.0.1:8765`.

## Tailscale (futuro)

- MagicDNS para nome da maquina;
- Tailscale Serve para HTTPS sobre o servico local;
- nome amigavel no tailnet (ex.: `https://mrp-trabalho.<tailnet>.ts.net`).

## Regras

- `8765` continua porta interna/configuravel;
- nome amigavel/proxy e camada de infraestrutura, nao regra de negocio;
- IP, hostname e porta nao devem ficar hardcoded em logica de negocio;
- ocultar IP/porta melhora usabilidade e reduz exposicao visual, mas nao substitui seguranca real.

## Ocultar IP/porta x seguranca real

Ocultar URL tecnica nao substitui:

- autenticacao;
- autorizacao/permissoes;
- firewall;
- segmentacao de rede;
- controle de acesso administrativo;
- logs e auditoria.

## Fora de escopo agora

- configurar proxy reverso;
- configurar DNS interno;
- configurar hosts em clientes;
- ativar Tailscale Serve/MagicDNS operacional;
- mudar frontend funcional.
