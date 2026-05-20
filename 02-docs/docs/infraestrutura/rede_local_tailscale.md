# Rede Local e Tailscale

Modelo atual: local-first.

- Rede local da empresa e acesso principal.
- Tailscale e acesso remoto tecnico.
- MEGA descontinuado na arquitetura.

URLs de referencia:

- Localhost: `http://localhost:8765`
- LAN: `http://IP_LOCAL_DO_SERVIDOR:8765`
- Tailscale: `http://IP_TAILSCALE_DO_SERVIDOR:8765`

Bind operacional atual:

`0.0.0.0` para atender LAN + Tailscale.

Nao abrir porta publica no roteador nesta fase.

## Diretriz futura - nome amigavel e proxy

Objetivo futuro: usuario final acessar o MRP por nome amigavel, sem expor IP/porta na URL.

Possibilidades futuras LAN:

- hosts local nos clientes;
- DNS interno (ex.: `mrp.local` ou `mrp.empresa.local`);
- proxy reverso local em 80/443 encaminhando para `127.0.0.1:8765`.

Possibilidades futuras Tailscale:

- MagicDNS para nome da maquina;
- Tailscale Serve para HTTPS com nome amigavel (ex.: `https://mrp-trabalho.<tailnet>.ts.net`).

Regra:

- `8765` permanece interna/configuravel;
- nome amigavel/proxy e camada de infraestrutura, nao regra de negocio;
- nao implementar nesta etapa documental.
