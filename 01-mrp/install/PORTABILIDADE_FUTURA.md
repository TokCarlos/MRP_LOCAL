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
