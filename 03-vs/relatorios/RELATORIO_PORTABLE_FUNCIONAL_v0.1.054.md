# RELATORIO PORTABLE FUNCIONAL v0.1.054

Data: 2026-05-21
Escopo: ajustar `portable` para pacote funcional de teste, sem depender da arvore DEV em execucao.

## 1. O que foi copiado para portable

- `01-mrp/front_end` -> `portable/app/frontend`
- `01-mrp/back_end` -> `portable/app/backend`
- `01-mrp/config` -> `portable/infrastructure/config`
- `01-mrp/back_end/app/domain` -> `portable/core/domain`
- `01-mrp/back_end/app/services` -> `portable/core/services`
- `01-mrp/core/engine` -> `portable/core/engine`
- `01-mrp/back_end/app/adapters` -> `portable/infrastructure/adapters`
- `01-mrp/back_end/app/repositories` e `01-mrp/db` -> `portable/infrastructure/persistence`
- `01-mrp/health` -> `portable/operations/health`
- `03-vs/scripts/servicos` -> `portable/operations/scripts`
- `01-mrp/tools` -> `portable/operations/tools` (com `validate_environment.ps1` local)
- `01-mrp/assets/icons` -> `portable/assets/icons`
- `01-mrp/front_end/img` -> `portable/assets/images`
- dados de `01-mrp/front_end/data` distribuídos em:
  - `portable/data/seed`
  - `portable/data/mock`
  - `portable/data/reference`
- `01-mrp/runtime` -> `portable/runtime`

## 2. O que foi excluido do portable

- conteudo que nao pertence ao pacote funcional:
  - `.git`, `.codex`, `02-docs`, `03-vs`, `00-manual-dev`, quarentena
  - `__pycache__`, `*.pyc`, `Thumbs.db`
  - logs reais antigos, temporarios antigos, backups/lixo operacional

## 3. O que foi mantido

- scripts oficiais de rede/validacao:
  - `01_configurar_share_sistema_mrp_admin.ps1`
  - `02_mapear_x_sistema_mrp_usuario.bat`
  - `03_validar_ambiente_sistema_mrp.ps1`
- scripts de operacao local:
  - `start_mrp.bat`, `stop_mrp.bat`, `status_mrp.bat`, `healthcheck_mrp.bat`
- camada operacional de uso:
  - `MRP_MENU_SISTEMA.bat`
  - `MRP_PAINEL_SERVIDOR.cmd`
  - `MRP_PAINEL_SERVIDOR.vbs`
  - `CRIAR_ATALHO_PAINEL_SERVIDOR.bat`
  - `operations/painel/mrp_painel_controle.py`
  - `operations/painel/mrp_admin_auth_setup.py`
- estrutura funcional completa:
  - `app`, `core`, `infrastructure`, `operations`, `assets`, `data`, `runtime`, `logs`, `tmp`

## 4. Como executar

1. Entrar na pasta `portable`.
2. Rodar `start_mrp.bat`.
3. Validar com `status_mrp.bat`.
4. Validar resposta com `healthcheck_mrp.bat`.
5. Parar com `stop_mrp.bat`.

## 5. Validacoes feitas

- `git diff --check`: OK.
- verificacao de sujeira proibida no `portable`: OK.
- existencia de `portable/app/frontend`: OK.
- existencia de `portable/app/backend`: OK.
- existencia de `portable/start_mrp.bat`: OK.
- existencia de `portable/README_PORTABLE.txt`: OK.
- verificacao de script relativo (`%~dp0`) em scripts de execucao: OK.
- `portable/03_validar_ambiente_sistema_mrp.ps1`: OK.
- painel python do portable: parse OK.
- validacao de sujeira proibida no portable: OK.

## 6. Validacoes pendentes

- start/stop/status/healthcheck em maquina destino real.
- backend no destino com `fastapi` + `uvicorn` disponiveis no Python local.

## 7. Riscos

- backend pode nao subir em maquina sem dependencias Python de API.
- scripts de rede (`01_` e `02_`) mantem caminhos de infraestrutura controlados por regra.
- diferencas de firewall/antivirus podem afetar bind de porta em outro PC.
- atalho depende de permissao do usuario para escrever na area de trabalho.

## 8. Proximo passo

1. Copiar apenas a pasta `portable` para maquina destino.
2. Rodar `start_mrp.bat`.
3. Rodar `healthcheck_mrp.bat`.
4. Se backend nao subir, manter fluxo de frontend e instalar dependencias backend em etapa controlada.
