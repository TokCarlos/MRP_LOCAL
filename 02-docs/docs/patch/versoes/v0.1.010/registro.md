# Registro v0.1.010 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `ACESSO_MOBILE_TAILSCALE_VALIDADO`

## Objetivo

Registrar o teste de acesso mobile ao front-end do `MRP_LOCAL` via Tailscale.

## Ambiente registrado

- PC/SERVIDOR: `home-machine`.
- IP Tailscale do PC: `100.108.26.10`.
- Telefone: `m15-de-carlos-alberto`.
- IP Tailscale do telefone: `100.90.190.4`.

## URL validada

`http://100.108.26.10:8000/login.html`

## Comando oficial

```powershell
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"
```

## Resultado

Acesso mobile via Tailscale validado.

## Observacoes

- Subnet routes nao foram necessarios.
- O problema anterior era que o telefone aparecia offline no Tailscale.
- Depois que o telefone ficou online, o acesso funcionou.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Apenas documentacao: SIM.

## Arquivos documentais desta etapa

- `02-docs/docs/patch/versoes/v0.1.010/registro.md`.
- `02-docs/docs/patch/versoes/v0.1.010/teste_mobile_tailscale.md`.
- `02-docs/docs/geral/acesso_local_e_tailscale.md`.
