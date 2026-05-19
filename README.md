
# MRP_LOCAL

Sistema local-first do projeto MRP.

## Estado atual

- Frontend estático em `01-mrp/front_end`.
- Porta operacional configurada: `8765`.
- Bind configurado: `0.0.0.0`.
- Dados atuais: mock/seed local, sem banco real.
- Backend real ainda não iniciado.
- Sistema ainda não deve ser chamado de blindado sem validação real em Windows.

## Estrutura oficial

- `01-mrp`: sistema operacional atual.
- `02-docs`: documentação, regras e histórico técnico útil.
- `03-vs`: scripts, empacotamento, releases, relatórios e apoio de versionamento.

## Regras absolutas

Leia `REGRAS_MRP.txt` antes de qualquer execução grande.

## Comandos principais

Status:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_status.ps1"
```

Iniciar frontend:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_start.ps1"
```

Healthcheck:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1"
```

Watchdog contínuo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_watchdog.ps1"
```

Instalar tarefa Windows no logon:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\servicos\mrp_frontend_task_install.ps1" -Schedule ONLOGON
```

## Futuro empacotamento

O projeto deve evoluir para instalação padrão de programa: precheck, runtime, cópia dos arquivos, configuração, firewall, tarefa/watchdog, healthcheck e relatório final. A regra de negócio deve continuar independente do instalador e do ambiente físico.
