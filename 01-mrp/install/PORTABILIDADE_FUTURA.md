# Portabilidade futura do MRP_LOCAL

Status: preparacao pos-CIMASP, sem instalador real.

## Objetivo

Preparar o caminho para empacotar o MRP_LOCAL em uma maquina nova sem depender do ambiente DEV.

## O que sera empacotado junto

- `01-mrp/front_end` funcional.
- `01-mrp/config` com configuracoes de ambiente.
- `01-mrp/install` com prechecks e orientacao de instalacao.
- `01-mrp/health` com validacoes de saude.
- `01-mrp/docs_runtime` com documentacao do pacote transportavel.
- Futuramente: runtime portatil, API, engine, adaptadores e scripts de servico.

## O que podera ser portatil

- Python portable em `01-mrp/runtime/python`.
- Node portable, se o frontend futuro exigir build local.
- Scripts PowerShell do proprio pacote.
- Configuracoes locais sem credenciais reais.

## O que podera exigir instalador externo

- Python, enquanto runtime portatil nao existir.
- PostgreSQL, quando banco real for aprovado.
- Tailscale, para acesso remoto.
- Regras de firewall, dependendo da permissao do Windows.

## Como detectar dependencias ausentes

Usar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\01-mrp\install\mrp_install_precheck.ps1"
```

O precheck verifica estrutura, config, `front_end/index.html`, porta, Python/runtime e permissao de escrita em pastas operacionais.
O precheck e passivo: nao instala dependencias, nao cria backend e nao cria banco.

## Porta e firewall

Porta oficial atual do frontend: `8765`.

Firewall deve liberar entrada TCP na rede privada. A regra atual fica nos scripts de servico em `03-vs`, mas o instalador futuro deve ter rotina propria.

## Runtime

Nesta etapa nada e baixado. O runtime futuro deve ficar em `01-mrp/runtime` e nao deve misturar dependencias com codigo-fonte.
Python portable e apenas direcao futura; nao foi ativado ainda.

## Atalho e menu

O instalador futuro pode criar atalho para iniciar o menu ou abrir a URL local do sistema.

## Tarefa automatica futura

A tarefa Windows deve iniciar o watchdog ou servico equivalente. Ainda precisa validacao real de logon, reboot e queda de energia.

## Estado real da etapa v0.1.045

- frontend funcional preservado na porta 8765;
- backend FastAPI ainda nao operacional;
- PostgreSQL ainda nao instalado/configurado pelo sistema;
- sistema ainda nao pode ser chamado de blindado/homologado.

## Estado real adicional da etapa v0.1.047

- deploy no trabalho validado;
- acesso por outras maquinas da rede validado;
- acesso remoto via Tailscale validado;
- pacote protegido v0.1.046 validado no trabalho;
- start/stop/status corrigidos e validados.

Area operacional auxiliar:

- pasta `portable` preservada como area oficial de apoio para deploy/teste/acesso externo;
- `portable\CONFIGURAR_ACESSO_MRP_REDE.bat` usado para alinhamento de clientes e bypass de proxy quando aplicavel;
- IP LAN de teste: `192.168.1.71`;
- IP Tailscale de teste: `100.117.224.127`;
- IPs de teste nao sao regra fixa do sistema.

Planejamento registrado:

- proxima etapa planejada: validacao operacional no DEV casa com painel admin local;
- etapa seguinte planejada: watchdog/tarefa automatica/reboot.

Preparacao adicional v0.1.049:

- painel administrativo local separado do frontend final;
- credencial local admin em `01-mrp/config/local/admin_auth.local.json` (nao versionar);
- chave local de modo automatico em `01-mrp/config/local/mrp_auto_mode.local.json` (nao versionar);
- watchdog futuro deve obedecer a chave administrativa local.

## Start, stop e healthcheck

Antes de release, validar:

- start;
- stop;
- restart;
- healthcheck;
- porta 8765;
- acesso local;
- acesso via rede;
- acesso via Tailscale, quando aplicavel.

## DEV x RELEASE

Pacote DEV:
- contem docs, scripts, relatorios e historico.

Pacote RELEASE:
- deve conter somente runtime, frontend, config, health, install, docs_runtime e servicos necessarios.
- nao deve conter logs reais, cache, tmp, backups locais, banco real ou arquivos de desenvolvimento desnecessarios.

## Direcao estrategica v0.1.050 - instalador unico

- objetivo futuro: distribuicao por instalador unico (exemplo conceitual: `MRP_LOCAL_Setup.exe`);
- nao implementar instalador real nesta etapa;
- nao gerar `.exe` nesta etapa;
- nao empacotar release nesta etapa.

Regras do instalador futuro:

- preparar ambiente e estrutura interna mantendo separacao de codigo, frontend, backend, engine, adapters, runtime, config, data, logs, backups e tmp;
- executar precheck antes de concluir;
- classificar pendencias em `CRITICO`, `OPCIONAL`, `RECOMENDADO`;
- bloquear conclusao em pendencia `CRITICO`;
- alertar/registrar e permitir continuidade para `OPCIONAL` e `RECOMENDADO` quando nao bloquear operacao;
- exigir aprovacao para acoes sensiveis (firewall, servico/tarefa Windows, permissoes, download externo, alteracao de ambiente);
- nao depender de `X:\`, `\\HOME-MACHINE`, usuario fixo ou unidade mapeada.

Decisao de ferramenta (Inno/NSIS/WiX/PyInstaller/cx_Freeze/outra) fica para etapa futura.

## Direcao estrategica complementar v0.1.050 - nome amigavel/proxy e IA futura

- objetivo futuro de usabilidade: acesso por nome amigavel (LAN/Tailscale/proxy), evitando URL final com IP:porta;
- a porta `8765` permanece como porta interna/configuravel do frontend;
- instalador/preparador futuro podera configurar hosts/DNS/proxy com aprovacao administrativa;
- ocultar IP/porta nao substitui seguranca real (autenticacao, firewall, Tailscale, backend e controle de acesso).

Integracao IA futura:

- deve ocorrer via backend/API, nao diretamente no frontend;
- deve usar ferramentas internas controladas, permissao e log;
- sem implementacao nesta etapa.

## Modelo futuro - programa Windows instalado

- DEV e release devem permanecer separados;
- repositorio DEV nao deve virar pasta poluida de build;
- release futuro pode conter executaveis (`.exe`) e dependencias (`.dll`, `.pyd`, `.bin`) com runtime interno;
- artefatos empacotados ficam fora do Git e sao gerados por etapa propria de release;
- backend Produtos continua como frente tecnica apos este registro documental.
