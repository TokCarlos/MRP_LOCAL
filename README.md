# MRP_LOCAL

Sistema local-first em ambiente de teste, com frontend web estatico validado localmente e preparacao inicial para portabilidade.

## Estado atual

- Versao documental: `v0.1.043-preparacao-portabilidade`.
- Base funcional anterior: `v0.1.042 recovery`.
- Commit base: `8c649e6 - chore: recovery funcional e saneamento operacional do MRP local`.
- Frontend validado pelo usuario: start OK, porta 8765 OK, healthcheck OK e sistema abrindo corretamente.
- Backend: ainda nao criado.
- Banco real: ainda nao criado.
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

Comando novo oficial em DEV:

```powershell
py -m http.server 8765 --bind 0.0.0.0 --directory "X:\01-mrp\front_end"
```

A porta antiga `8000` esta descontinuada e deve permanecer apenas como historico documental.

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