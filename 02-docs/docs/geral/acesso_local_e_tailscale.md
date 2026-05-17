# Acesso Local e Tailscale - MRP_LOCAL

Versao de referencia: v0.1.010
Data do registro: 2026-05-17
Status: `ACESSO_MOBILE_TAILSCALE_VALIDADO`

## Objetivo

Registrar o procedimento validado para acessar o front-end do `MRP_LOCAL` pela rede Tailscale.

## Estrutura usada

- Sistema principal: `X:\01-mrp\front_end`.
- Servidor local: Python HTTP server.
- PC/SERVIDOR: `home-machine`.
- IP Tailscale do PC: `100.108.26.10`.
- Telefone testado: `m15-de-carlos-alberto`.
- IP Tailscale do telefone: `100.90.190.4`.

## Comando oficial no PC

Executar no PC/SERVIDOR:

```powershell
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"
```

## URL para acessar pelo telefone

```text
http://100.108.26.10:8000/login.html
```

## Resultado validado

A pagina `login.html` abriu corretamente no telefone via Tailscale.

## Subnet routes

Subnet routes nao foram necessarios neste cenario.

Motivo: o telefone acessou diretamente o IP Tailscale do PC (`100.108.26.10`) na porta `8000`.

## Diagnostico do problema anterior

O problema anterior era que o telefone aparecia offline no Tailscale. Depois que o telefone ficou online, o acesso funcionou.

## Checklist rapido

- [ ] Confirmar que o PC esta online no Tailscale.
- [ ] Confirmar que o telefone esta online no Tailscale.
- [ ] Iniciar o servidor com bind no IP Tailscale do PC.
- [ ] Abrir `http://100.108.26.10:8000/login.html` no telefone.
- [ ] Se falhar, verificar se o telefone aparece offline no Tailscale.

## Regras

- Este procedimento nao cria backend.
- Este procedimento nao cria banco.
- Este procedimento nao altera codigo funcional.
- Este procedimento serve apenas o front-end existente para teste local/remoto controlado.
