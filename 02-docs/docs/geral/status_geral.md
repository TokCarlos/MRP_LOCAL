# Status Geral - MRP_LOCAL

## Versao documental atual

`v0.1.049-fix-launcher-painel-admin`

## Base funcional anterior

`v0.1.049 painel admin local preparacao`

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
- Painel Administrativo Local com launcher clicavel, separado do frontend final.

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

## Atualizacao pre-backend v0.1.056

- DEV passou por saneamento operacional (cache Python, logs reais e BOM tecnico tratados).
- Portable ficou apenas com limpeza operacional nesta etapa (sem avancar escopo funcional).
- Estrutura nova (`app/core/infrastructure/operations`) permanece parcial.
- `front_end` e `back_end` seguem ativos por compatibilidade nesta fase.
- Proximo foco tecnico: etapa Backend.
- O sistema continua NAO homologado e NAO blindado.

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

## Etapa atual em andamento: v0.1.049-fix-launcher

- correcao de usabilidade do launcher do painel admin por duplo clique;
- adicao de launcher principal VBS e launcher diagnostico CMD;
- modernizacao visual do painel tkinter/ttk sem dependencias externas;
- script de criacao de atalho para area de trabalho.

## Status final desta etapa

`PAINEL_ADMIN_LOCAL_COM_LAUNCHER_FUNCIONAL_SEM_ATIVACAO_AUTOMATICA`

## Planejamento

- proxima etapa planejada: `validacao operacional no DEV casa com painel admin local`;
- etapa seguinte planejada: `watchdog/tarefa automatica/reboot`.

## Etapa v0.1.050 - regra instalador futuro (documental)

- registrada diretriz estrategica para instalador unico de distribuicao;
- sem implementacao de instalador real nesta etapa;
- sem geracao de `.exe` nesta etapa;
- sem backend novo, sem banco novo e sem alteracao funcional do frontend;
- tecnologia do instalador ainda nao definida;
- sistema segue em teste/desenvolvimento e ainda nao e blindado.

## Etapa v0.1.050 - registro futuro dominio/proxy e IA (documental)

- registrada diretriz de acesso futuro por nome amigavel/proxy para ocultar IP e porta do usuario final;
- mantida regra de porta interna/configuravel `8765`;
- registrada diretriz de integracao IA futura via backend com ferramentas controladas;
- confirmacao de que nada foi implementado: sem proxy, sem DNS, sem Tailscale Serve, sem backend novo, sem banco novo, sem IA integrada;
- sem criacao de segredo/token/API key;
- sistema continua em teste/desenvolvimento e ainda nao e blindado.

## Etapa v0.1.051 - backend Produtos contrato/base (tecnica sem ativacao)

- definido papel do modulo Produtos como primeiro dominio real do backend;
- definido modelo logico inicial (empresas, atas, categorias, produtos);
- contrato planejado publicado em `01-mrp/back_end/contracts/produtos_api.v0.1.json`;
- criada base Python padrao para adapter/repository/service/teste do seed;
- criado diagnostico `03-vs/scripts/backend/validar_backend_produtos_seed.py`;
- sem FastAPI ativo, sem banco real e sem alteracao funcional de frontend/painel.

## Registro documental - modelo futuro de programa Windows

- registrado objetivo futuro de release instalado com instalador unico;
- registrada diferenca entre repositorio DEV e artefato de programa instalado;
- confirmado que nao houve criacao de `.exe`, `.dll`, `.bin` ou runtime empacotado nesta etapa;
- confirmada continuidade da frente tecnica do backend Produtos apos este registro.

## Etapa v0.1.050 - icons dll launcher

- pacote de icones incorporado em `01-mrp/assets/icons/windows`;
- etapa historica (DLL nao e padrao atual de atalho);
- fallback para icone padrao do Windows quando a DLL nao existir;
- alteracao restrita a recurso visual de launcher.

## Etapa v0.1.052 - icones oficiais .ico launcher

- problema: icone da DLL aparecia em propriedades, mas nao renderizava de forma confiavel na area de trabalho;
- decisao: usar `.ico` direto multi-resolucao como padrao do atalho;
- 4 icones oficiais gerados em `01-mrp/assets/icons/windows/ico`;
- atalho do painel aponta para `mrp_mrp_dark.ico` com fallback para `mrp_pcp_light.ico`;
- DLL mantida apenas como recurso opcional/futuro.

## Correcao definitiva de atalho visual do painel

- conceito corrigido: `.vbs` e launcher interno, `.lnk` e item visual oficial;
- atalho passa a usar `wscript.exe` como alvo e `MRP_PAINEL_SERVIDOR.vbs` em argumentos;
- icone vem de `.ico` local em `%LOCALAPPDATA%\MRP_LOCAL\icons`;
- criado script de diagnostico para validar `TargetPath`, `Arguments`, `WorkingDirectory` e `IconLocation`.

## Saneamento v0.1.052b - dev, icones e pacote

- limpeza de lixo operacional DEV (pycache, pyc, logs reais e zip transitorio);
- preservados os 4 icones oficiais atuais;
- removidos artefatos antigos de DLL sem uso operacional atual;
- adapter de Produtos com path de imagem mais portavel;
- criado script de pacote limpo para upload/revisao.

## Etapa v0.1.053 - backend minimo + API Produtos

- backend minimo consolidado em `01-mrp/back_end/app`;
- endpoints ativos quando iniciado:
  - `GET /health`
  - `GET /api/status`
  - `GET /api/produtos`
- sem banco real, sem CRUD completo e sem autenticacao nova;
- scripts de operacao backend criados em `03-vs/scripts/servicos`;
- frontend Produtos ajustado para consumir API primeiro com fallback explicito.

## Etapa v0.1.053b - refatoracao arquitetural e limpeza pos-backend inicial

- backend oficial unico consolidado em `01-mrp/back_end`;
- estrutura temporaria `01-mrp/backend` removida apos migracao util;
- Produtos padronizado como modulo-template:
  - route -> service -> repository/adapter -> domain/contracts -> seed;
- resposta de `GET /api/produtos` padronizada em:
  - `{ ok, source, count, items }`;
- sem banco real, sem CRUD completo e sem alteracao de seed/imagens.

## Atualizacao Produtos BOM v0.1.053 (2026-05-20 01:32:03 -03:00)

- Fluxo visual implantado: Produtos -> BOM (por produto selecionado).
- Tabela Produtos no frontend com colunas:
  ID | PREVIEW | ATA + NUMERO | PRODUTO | EMPRESA | ACAO.
- Acao visual da linha: botao "BOM".
- Tela BOM com 3 tabelas:
  - TUBOS (com TAMANHO)
  - CHAPAS (com TAMANHO)
  - INSUMOS (com UNIDADE)
- Implementacao provisoria com dados mock controlados.
- Sem banco real e sem persistencia definitiva nesta etapa.
- Estado do sistema: funcional em teste, nao homologado.

## Etapa v0.1.054 - saneamento estrutural e regras de ambiente

- raiz fisica oficial atual registrada: `C:\Users\carlo\Desktop\PCP SERVIDOR\SISTEMA_MRP`;
- pasta `C:\Users\carlo\Desktop\PCP SERVIDOR\PCP` registrada como proibida/intocavel;
- raiz direta em `C:\` bloqueada para uso como raiz do MRP_LOCAL;
- caminho operacional `\\HOME-MACHINE\system_jpl` e unidade `X:\` tratados como ambiente DEV/teste;
- share `system_jpl` deve apontar somente para a raiz fisica oficial;
- portable deve permanecer minimo, sem historico pesado, logs reais, quarentena, `.git` ou `.codex`;
- quarentena oficial fica em `03-vs/quarentena`;
- modulos devem ser desacoplados, com dependencia explicita e validacao propria;
- sistema permanece local-first, em teste, nao homologado e nao blindado.
