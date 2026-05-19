# MRP_LOCAL

Sistema local-first em ambiente de teste, com frontend web estatico funcional e etapa de preparacao de portabilidade pos-CIMASP.

## Estado atual

- Versao documental: `v0.1.045-preparacao-portabilidade-pos-cimasp`.
- Base anterior concluida: `v0.1.044 imagens CIMASP`.
- Commit base da etapa anterior: `60e5d6e - v0.1.044 - Cataloga imagens CIMASP`.
- Frontend validado pelo usuario: start OK, porta 8765 OK, healthcheck OK e sistema abrindo corretamente.
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
