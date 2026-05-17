# Teste Mobile Tailscale - v0.1.010

Data do registro: 2026-05-17
Status: `ACESSO_MOBILE_TAILSCALE_VALIDADO`

## Dispositivos

### PC/SERVIDOR

- Nome: `home-machine`.
- IP Tailscale: `100.108.26.10`.

### Telefone

- Nome: `m15-de-carlos-alberto`.
- IP Tailscale: `100.90.190.4`.

## Servidor local usado

Pasta servida:

`X:\01-mrp\front_end`

Comando oficial:

```powershell
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"
```

## URL validada no telefone

`http://100.108.26.10:8000/login.html`

## Resultado

A pagina `login.html` abriu no telefone via Tailscale.

## Subnet routes

Subnet routes nao foram necessarios para este teste, porque o acesso foi feito diretamente pelo IP Tailscale do PC.

## Problema anterior

- O telefone aparecia offline no Tailscale.
- Enquanto o telefone estava offline, o acesso nao funcionava.
- Depois que o telefone ficou online no Tailscale, o acesso funcionou.

## Conclusao

O acesso mobile ao front-end do `MRP_LOCAL` via Tailscale foi validado usando o IP Tailscale do PC e servidor HTTP local apontando para `X:\01-mrp\front_end`.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Apenas documentacao: SIM.
