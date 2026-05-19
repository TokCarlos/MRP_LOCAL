# Status Geral - MRP_LOCAL

## Versao documental atual

`v0.1.044-catalogacao-imagens-cimasp`

## Base funcional anterior

`v0.1.042 recovery`

Commit base funcional:

`8c649e6 - chore: recovery funcional e saneamento operacional do MRP local`

## Estado real atual

- Frontend validado pelo usuario: start OK, porta 8765 OK, healthcheck OK e sistema abrindo corretamente.
- O sistema ainda NAO esta blindado.
- O sistema ainda NAO esta homologado.
- Ainda nao ha backend FastAPI.
- Ainda nao ha banco real.
- Nao ha PostgreSQL criado nesta etapa.
- Nao ha instalador real criado nesta etapa.

## Pendencias de blindagem

Ainda precisam validacao real:

- watchdog continuo;
- tarefa Windows;
- logoff/logon;
- reboot;
- queda de energia;
- queda de rede;
- persistencia da raiz em contexto automatico;
- logs reais em execucao prolongada;
- pacote DEV separado de pacote RELEASE.

## Infraestrutura atual

- Frontend estatico em `01-mrp/front_end`.
- Porta oficial: `8765`.
- Porta antiga `8000`: descontinuada.
- Bind operacional: `0.0.0.0`.
- Acesso remoto: Tailscale.
- Acesso principal: rede local.
- MEGA: descontinuado como arquitetura.

## Portabilidade v0.1.043

Preparada estrutura inicial dentro de `01-mrp` para futuro empacotamento/instalador:

- `config`
- `runtime`
- `tools`
- `data`
- `db`
- `logs`
- `tmp`
- `backups`
- `front_end`
- `back_end`
- `engine`
- `adapters`
- `install`
- `health`
- `docs_runtime`

Essa estrutura e apenas preparatoria. Nao cria backend, nao cria banco e nao altera a regra funcional do frontend validado.

## Scripts/prechecks novos

- `01-mrp/install/mrp_install_precheck.ps1`
- `01-mrp/health/mrp_health_precheck.ps1`

Esses scripts verificam estrutura, config, frontend/index, porta, Python/runtime e permissao de escrita. Eles nao instalam dependencias, nao criam banco e nao iniciam backend.

## Regra de ambiente

A raiz fisica atual de desenvolvimento pode existir em documentacao, config e scripts de ambiente, mas nao pode virar regra de negocio. Scripts novos de portabilidade resolvem a raiz dinamicamente pela propria posicao.

## Status final desta etapa

`PREPARACAO_PORTABILIDADE_INICIAL`

## Catalogacao imagens CIMASP v0.1.044

- ATA CIMASP 029/2025 migrada de previews SVG DEMO para PNG REAL_ATA.
- Variacoes de itens registradas com sufixo `-1` quando havia imagem adicional no ZIP.
- Nomes oficiais preservados a partir dos registros existentes.
