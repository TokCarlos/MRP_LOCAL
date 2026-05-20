# MRP_LOCAL

Sistema local-first em ambiente de teste, com frontend web estatico funcional e painel administrativo local separado para o servidor.

## Estado atual

- Versao documental: `v0.1.049-fix-launcher-painel-admin`.
- Base anterior concluida: `v0.1.049 painel admin local preparacao`.
- Commit base relevante anterior: `173456b - chore: preparar portabilidade pos-cimasp v0.1.045`.
- Frontend validado pelo usuario: start OK, porta 8765 OK, healthcheck OK e sistema abrindo corretamente.
- Deploy no trabalho validado.
- Acesso por outras maquinas da rede validado.
- Acesso remoto via Tailscale validado.
- Backend real: ainda nao criado.
- Banco real: ainda nao criado.
- PostgreSQL: ainda nao instalado/configurado pelo sistema.
- Python portable: ainda nao baixado/ativado pelo sistema.
- FastAPI funcional: ainda nao criada.
- Sistema: ainda nao blindado/homologado.

## Estrutura principal

- `01-mrp`: nucleo executavel.
- `02-docs`: documentacao e historico.
- `03-vs`: scripts, relatorios, patches e versionamento.
- `00-manual-dev`: manual e resumo operacional do dono/dev.

## Frontend atual

Diretorio:

```text
01-mrp/front_end
```

Porta oficial:

```text
8765
```

Operacao principal:

- `MRP_MENU_SISTEMA.bat`
- `03-vs/scripts/servicos/mrp_frontend_start.ps1`
- `03-vs/scripts/servicos/mrp_frontend_stop.ps1`
- `03-vs/scripts/servicos/mrp_frontend_status.ps1`
- `03-vs/scripts/servicos/mrp_frontend_healthcheck.ps1`

Separacao de interface:

- `index.html` permanece interface de usuario final;
- painel administrativo local fica separado em `03-vs/scripts/painel/mrp_painel_controle.py`.

Launchers do painel admin local:

- principal: `MRP_PAINEL_SERVIDOR.vbs` (duplo clique)
- diagnostico: `MRP_PAINEL_SERVIDOR.cmd`
- compatibilidade: `MRP_MENU_SISTEMA.bat`
- criar atalho: `CRIAR_ATALHO_PAINEL_SERVIDOR.bat` ou `03-vs/scripts/painel/criar_atalho_painel.ps1`

## Area portable

A pasta `portable` e area operacional auxiliar para deploy/teste/acesso em maquinas clientes.

Arquivos operacionais relevantes em `portable`:

- `CONFIGURAR_ACESSO_MRP_REDE.bat`
- `COLINHA_EXECUCAO_PC_TRABALHO_MRP_ATUALIZADA.txt`
- `MRP_TRABALHO_PRECHECK.bat`
- `MRP_TRABALHO_FIREWALL_ADMIN.bat`
- `MRP_TRABALHO_STATUS.bat`
- `MRP_TRABALHO_PROTEGER_PASTA_ADMIN.bat`
- `MRP_TRABALHO_RESTAURAR_PERMISSOES_ADMIN.bat`
- `LEIA_INSTALACAO_PC_TRABALHO.txt`
- `LEIA_SEGURANCA_PC_TRABALHO.txt`
- `LEIA_FIX_START_STOP_STATUS.txt`

`CONFIGURAR_ACESSO_MRP_REDE.bat`:

- ferramenta operacional auxiliar (nao e core de regra de negocio);
- testa/acessa o servidor MRP por LAN e/ou Tailscale;
- ajusta excecoes de proxy/bypass no usuario do Windows;
- gera log local em `%LOCALAPPDATA%`;
- IP LAN usado no teste: `192.168.1.71`;
- IP Tailscale usado no teste: `100.117.224.127`;
- esses IPs sao dados operacionais de teste, nao regra fixa do sistema.

## Painel Administrativo Local (v0.1.049)

- uso exclusivo no servidor/PC onde o MRP roda;
- nao exposto como controle administrativo via navegador;
- acoes administrativas exigem credencial local;
- credencial real local: `01-mrp/config/local/admin_auth.local.json` (nao versionar);
- chave de modo automatico local: `01-mrp/config/local/mrp_auto_mode.local.json` (nao versionar);
- watchdog futuro deve obedecer essa chave administrativa.

Observacao tecnica:

- `py -m http.server` pode ser usado somente para diagnostico pontual, nao como operacao principal.
- A porta antiga `8000` esta descontinuada e deve permanecer apenas como historico documental.

## Scripts principais

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_start.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_stop.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_status.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1
```

## Prechecks de portabilidade

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\01-mrp\install\mrp_install_precheck.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\01-mrp\health\mrp_health_precheck.ps1
```

## Regras

Antes de alterar o projeto, ler `REGRAS_MRP.txt`.

Nao criar backend, banco real ou nova regra funcional sem tarefa explicita.

Nao chamar o sistema de blindado antes de validar watchdog, tarefa automatica, reboot, queda de energia, queda de rede, logs e healthcheck continuo.

Planejamento registrado:

- proxima etapa planejada: `validacao operacional no DEV casa com painel admin local`;
- etapa seguinte planejada: `watchdog/tarefa automatica/reboot`.

## Regra estrategica v0.1.050 (instalador futuro)

- objetivo futuro: distribuicao por instalador unico (exemplo conceitual: `MRP_LOCAL_Setup.exe`);
- nesta etapa nao ha implementacao de instalador, `.exe` ou empacotamento release;
- instalador futuro deve executar precheck e classificar pendencias em `CRITICO`, `OPCIONAL`, `RECOMENDADO`;
- acoes sensiveis devem exigir aprovacao (firewall, servico/tarefa Windows, permissao, download e alteracoes de ambiente);
- instalador futuro nao pode depender de `X:\`, `\\HOME-MACHINE`, usuario especifico ou drive mapeado;
- tecnologia do instalador fica para etapa futura.

## Regra estrategica v0.1.050 (nome amigavel/proxy e IA futura)

- objetivo futuro de acesso: trocar `http://IP:8765/index.html` por nome amigavel (LAN/Tailscale/proxy);
- exemplos conceituais: `http://mrp.local`, `https://mrp.local`, `https://mrp-trabalho.<tailnet>.ts.net`;
- a porta `8765` permanece interna/configuravel;
- proxy/dominio interno e camada de infraestrutura, nao regra de negocio;
- integracao IA futura deve ser via backend/API, nunca com chave no frontend;
- IA futura deve usar ferramentas controladas, permissao, confirmacao para acoes criticas e log obrigatorio;
- nao implementar proxy, DNS, Tailscale Serve nem IA nesta etapa.

## Etapa v0.1.051 (backend Produtos base)

- inicia a base tecnica do backend para o modulo Produtos;
- define contrato de API planejado e modelo logico inicial;
- mantem `produtos_seed.json` como fonte temporaria;
- sem FastAPI ativo e sem banco real nesta etapa;
- frontend e painel admin permanecem preservados.

## Registro futuro - programa Windows instalado

- objetivo futuro: distribuicao como programa Windows instalado com instalador unico;
- exemplo conceitual de release: `MRP_LOCAL_Setup.exe`, `MRP_Server.exe`, `MRP_Painel.exe`, `runtime/`, `app/`, `config/`, `data/`, `logs/`, `db/`;
- `.dll`, `.pyd` e `.bin` podem existir no release futuro como dependencias/runtime;
- isso nao altera o repositorio DEV atual, que deve permanecer limpo e modular;
- backend Produtos continua como proxima frente tecnica.

## Etapa visual launcher (v0.1.050 icons dll)

- registro historico: pacote DLL foi incorporado em etapa anterior;
- padrao atual do atalho nao usa DLL;
- DLL de icones e historica/opcional/futura.

## Etapa visual launcher (v0.1.052 icones oficiais .ico)

- atalho do painel passou a usar `.ico` direto multi-resolucao;
- 4 icones oficiais em `01-mrp/assets/icons/windows/ico`:
  - `mrp_pcp_light.ico`
  - `mrp_jpl_dark.ico`
  - `mrp_mrp_light.ico`
  - `mrp_mrp_dark.ico`
- padrao atual do atalho: `mrp_mrp_dark.ico` (fallback `mrp_pcp_light.ico`);
- DLL de icones permanece opcional/futura e nao e caminho principal do atalho.

## Ajuste definitivo de atalho visual

- `.vbs` e launcher operacional interno e nao item visual final;
- item visual oficial e `MRP_LOCAL - Painel do Servidor.lnk`;
- atalho aponta para `wscript.exe` com argumento para o `.vbs`;
- icone do atalho usa `.ico` local em `%LOCALAPPDATA%\MRP_LOCAL\icons`.

## Saneamento v0.1.052b

- icones oficiais preservados: `mrp_pcp_light`, `mrp_jpl_dark`, `mrp_mrp_light`, `mrp_mrp_dark`;
- artefatos antigos de DLL removidos do caminho oficial de uso;
- backend Produtos permanece sem FastAPI ativo e sem banco;
- adapter de seed com resolucao de path de imagem mais portavel;
- pacote para upload/revisao deve ser gerado por `GERAR_PACOTE_LIMPO_DEV.bat`.
- pacote limpo exclui `.git`, `.codex`, logs reais, cache, `__pycache__`, `*.pyc`, `Thumbs.db` e zips transitarios.

## Etapa v0.1.053 (backend minimo + API Produtos)

- backend FastAPI minimo consolidado em `01-mrp/back_end/app`;
- endpoints:
  - `GET /health`
  - `GET /api/status`
  - `GET /api/produtos`
- sem banco real, sem CRUD completo e sem autenticacao nova;
- aba Produtos passa a tentar API backend primeiro e usa fallback explicito (seed/local mock) quando a API falha;
- scripts operacionais backend:
  - `03-vs/scripts/servicos/mrp_backend_start.ps1`
  - `03-vs/scripts/servicos/mrp_backend_status.ps1`
  - `03-vs/scripts/servicos/mrp_backend_healthcheck.ps1`
  - `03-vs/scripts/servicos/mrp_backend_stop.ps1`

## Etapa v0.1.053b (refatoracao arquitetural back_end)

- backend oficial consolidado em `01-mrp/back_end` (estrutura `01-mrp/backend` removida por ser temporaria/legado);
- fluxo Produtos padronizado: `route -> service -> repository/adapter -> domain/contracts -> seed`;
- resposta de `GET /api/produtos` padronizada em `{ ok, source, count, items }`;
- sem banco real, sem CRUD completo e sem alteracao de seed/imagens.
