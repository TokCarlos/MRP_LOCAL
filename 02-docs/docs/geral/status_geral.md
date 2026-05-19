# Status Geral - MRP_LOCAL

## Versao documental atual

`v0.1.048-alinhamento-regras-status-operacional`

## Base funcional anterior

`v0.1.047 registro deploy trabalho e teste DEV`

Commit base funcional:

`173456b - chore: preparar portabilidade pos-cimasp v0.1.045`

## Estado real atual

- Frontend validado pelo usuario: start OK, porta 8765 OK, healthcheck OK e sistema abrindo corretamente.
- Deploy no trabalho validado.
- Acesso local no trabalho validado.
- Acesso por outras maquinas da rede validado com script auxiliar.
- Acesso remoto via Tailscale validado.
- Pacote protegido v0.1.046 validado no trabalho.
- Start/stop/status corrigidos e validados.
- O sistema ainda NAO esta blindado.
- O sistema ainda NAO esta homologado.
- Ainda nao ha backend FastAPI funcional.
- Ainda nao ha banco real.
- Nao ha PostgreSQL instalado/configurado pelo sistema.
- Nao ha Python portable baixado/ativado pelo sistema.
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
- IP LAN usado no teste operacional: `192.168.1.71`.
- IP Tailscale usado no teste operacional: `100.117.224.127`.
- Os IPs de teste nao sao regra fixa do sistema.

## Area portable (preservada)

A pasta `portable` e area oficial de apoio operacional para deploy/teste/acesso em maquinas clientes.

Arquivos chave:

- `portable\CONFIGURAR_ACESSO_MRP_REDE.bat`
- `portable\COLINHA_EXECUCAO_PC_TRABALHO_MRP_ATUALIZADA.txt`
- `portable\MRP_TRABALHO_PRECHECK.bat`
- `portable\MRP_TRABALHO_FIREWALL_ADMIN.bat`
- `portable\MRP_TRABALHO_STATUS.bat`
- `portable\MRP_TRABALHO_PROTEGER_PASTA_ADMIN.bat`
- `portable\MRP_TRABALHO_RESTAURAR_PERMISSOES_ADMIN.bat`
- `portable\LEIA_INSTALACAO_PC_TRABALHO.txt`
- `portable\LEIA_SEGURANCA_PC_TRABALHO.txt`
- `portable\LEIA_FIX_START_STOP_STATUS.txt`

Observacoes:

- `CONFIGURAR_ACESSO_MRP_REDE.bat` e ferramenta operacional auxiliar, nao regra de negocio.
- Ele testa/acessa o servidor MRP por LAN/Tailscale, ajusta bypass de proxy no usuario e gera log local em `%LOCALAPPDATA%`.
- O arquivo permanece em `portable` e nao deve ser movido/copiado para a raiz.

## Portabilidade v0.1.045

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

## Etapa anterior concluida: v0.1.044

- ATA CIMASP 029/2025 migrada de previews SVG DEMO para PNG REAL_ATA.
- Variacoes de itens registradas com sufixo `-1` quando havia imagem adicional no ZIP.
- Nomes oficiais preservados a partir dos registros existentes.

## Etapa atual em andamento: v0.1.048

- alinhamento de regras e status operacional ao estado real atual;
- confirmacao de preservacao da pasta portable e arquivo CONFIGURAR_ACESSO_MRP_REDE.bat;
- consolidacao documental pre-proxima rodada operacional.

## Status final desta etapa

`ALINHAMENTO_REGRAS_E_STATUS_CONCLUIDO`

## Planejamento

- proxima etapa planejada: `v0.1.048 validacao operacional no DEV casa`;
- etapa seguinte planejada: `v0.1.049 watchdog/tarefa automatica/reboot`.
