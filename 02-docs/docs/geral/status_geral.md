
# Status Geral — MRP_LOCAL

## Estado consolidado

Projeto: MRP_LOCAL
Status: BASE LIMPA PARA RETOMADA DE DESENVOLVIMENTO
Versão documental: v0.1.037-saneamento
Homologação: NÃO HOMOLOGADO

## O que está funcional nesta base

- Frontend estático em `01-mrp/front_end`.
- Login/interface/mock local preservados.
- Porta configurada: `8765`.
- Bind configurado: `0.0.0.0`.
- Scripts de serviço passaram a usar configuração central e raiz resolvida, sem dependência direta de `X:\`.
- Healthcheck, start, stop, status, firewall, tarefa e watchdog foram reorganizados para padrão configurável.
- `REGRAS_MRP.txt` foi incorporado ao projeto como regra absoluta de execução.
- Logs reais, `Thumbs.db`, `.git`, `.codex`, quarentena pesada, snapshots e patches antigos foram removidos do pacote limpo.

## O que ainda não pode ser chamado de blindado

- Validação real em Windows após logoff/logon.
- Validação real após reboot.
- Validação real após queda de rede.
- Validação real após queda de energia.
- Validação real em outro PC da LAN.
- Validação real por Tailscale, se usado.
- Teste com Python portable/instalador final.

## Banco e backend

- Backend real ainda não iniciado.
- Banco real ainda não iniciado.
- Dados atuais continuam sendo mock/seed local.

## Regra de empacotamento futuro

O sistema deve evoluir para programa instalável/empacotado. Uma máquina limpa deve receber precheck, runtime necessário, arquivos do sistema, configuração, firewall, tarefa/watchdog, healthcheck e relatório final. O instalador prepara o ambiente; a regra de negócio permanece desacoplada.
