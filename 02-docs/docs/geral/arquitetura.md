# Arquitetura — MRP_LOCAL

## Padrão obrigatório

A arquitetura segue o padrão:

- Configuração
- Motor
- Adaptador

## Configuração

Define ambiente, porta, raiz, logs, runtime e tarefa.

Arquivo atual:

`01-mrp/config/mrp_local.env.json`

## Motor

Executa regra de negócio. Ainda não existe backend/engine real nesta fase.

## Adaptadores

Conectam o sistema ao ambiente externo:

- scripts de serviço Windows;
- firewall;
- tarefa Windows;
- watchdog;
- futuro instalador.

## Regra crítica

Regra de negócio não deve conhecer caminho físico, usuário Windows, drive mapeado, Tailscale ou IP. Isso pertence à configuração/adaptador.
