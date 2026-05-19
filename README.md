# MRP_LOCAL

Sistema local-first em ambiente de teste, com frontend web estatico funcional e deploy validado em ambiente de trabalho.

## Estado atual

- Versao documental: `v0.1.048-alinhamento-regras-status-operacional`.
- Base anterior concluida: `v0.1.047 registro deploy trabalho e teste DEV`.
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

- proxima etapa planejada: `v0.1.048 validacao operacional no DEV casa`;
- etapa seguinte planejada: `v0.1.049 watchdog/tarefa automatica/reboot`.
