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
