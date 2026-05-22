# RELATORIO_REESTRUTURACAO_DESACOPLAMENTO_v0.1.055

Data: 2026-05-21  
Escopo: desacoplamento, portable funcional, padronizacao de portas, validacoes basicas e ajuste de base para zoom/imagens.

## 1) Resumo executivo

- Foi consolidado `portable` como pacote funcional com `app/frontend` e `app/backend` internos, sem dependencia direta do DEV para start local.
- Foi criado resolver de paths por ambiente (`dev`/`portable`) com suporte a variaveis `MRP_*`.
- Foi padronizada a porta da API para `8876` nos scripts do portable.
- Foi mantida a regra de pasta proibida absoluta em `REGRAS_MRP.txt` (clausula permanente).
- O frontend portable sobe e responde em `8765`; backend portable nao subiu neste host por falta de dependencias Python (`fastapi/uvicorn`) no ambiente atual.

## 2) Estrutura antes/depois (pontos criticos)

Antes:
- Backend/config ainda acoplado a `01-mrp/front_end` e `01-mrp/back_end`.
- Scripts portable com backend em `8001`.
- Portable parcial com componentes novos e legados misturados.

Depois:
- Resolver de caminhos criado em:
  - `01-mrp/infrastructure/config/paths.py`
  - `portable/infrastructure/config/paths.py`
- Backend/config atualizado para priorizar `data/seed/produtos_seed.json` e fallback controlado.
- Scripts portable alinhados para backend `8876`.

## 3) Arquivos alterados principais

- `01-mrp/infrastructure/config/paths.py` (novo)
- `portable/infrastructure/config/paths.py` (novo)
- `01-mrp/back_end/app/config.py`
- `portable/app/backend/app/config.py`
- `portable/start_mrp.bat`
- `portable/status_mrp.bat`
- `portable/healthcheck_mrp.bat`
- `portable/README_PORTABLE.txt`
- `portable/MANIFEST_PORTABLE.txt`
- `portable/operations/painel/mrp_painel_controle.py`
- `portable/operations/painel/mrp_admin_auth_setup.py`

## 4) Dependencias antigas removidas (ativas)

- Porta backend `8001` removida dos scripts principais de start/status/healthcheck do portable.
- Referencia obrigatoria a seed em `01-mrp/front_end/data` removida como fonte primaria do backend; agora fonte primaria e `data/seed`.

## 5) Dependencias antigas mantidas por compatibilidade/documentacao

- Ocorrencias de `\\HOME-MACHINE\system_jpl` e `X:\` permanecem apenas nos scripts de infraestrutura/mapeamento de rede do portable.
- Ocorrencias de caminhos fisicos bloqueados permanecem em scripts validadores/documentos de controle.

## 6) Ajustes no portable

- Estrutura funcional mantida em `portable/app/frontend` e `portable/app/backend`.
- Ajuste de scripts para uso relativo (`%~dp0`) e logs/tmp/runtime locais do portable.
- Remocao de arquivos locais sensiveis em `portable/infrastructure/config/local` (mantido `.gitkeep`).

## 7) Ajustes no backend

- Configuracao de paths desacoplada com env vars:
  - `MRP_ROOT`, `MRP_MODE`, `MRP_FRONTEND_ROOT`, `MRP_BACKEND_ROOT`, `MRP_DATA_ROOT`, `MRP_ASSETS_ROOT`, `MRP_LOGS_ROOT`, `MRP_RUNTIME_ROOT`.
- Deteccao automatica de raiz em DEV/portable.

## 8) Ajustes no frontend / imagens / zoom

- Frontend de produtos segue com modal/lightbox ativo no clique de preview.
- Fluxo de fallback de imagem permanece com placeholder quando `src` falha.
- Base de imagens continua exigindo consolidacao final para fonte unica em `assets/images/produtos` (pendencia parcial).

## 9) Validacoes executadas

- `git diff --check`: OK
- `python -m compileall 01-mrp/back_end/app portable/app/backend/app portable/operations/painel`: OK
- `node --check 01-mrp/front_end/js/pages/produtos_list.js`: OK
- `node --check portable/app/frontend/js/pages/produtos_list.js`: OK
- Varredura de hardcode proibido em codigo ativo do portable (start/stop/status/health/config/app): sem ocorrencias proibidas.
- `portable/healthcheck_mrp.bat`: frontend OK, backend nao respondeu neste host.

## 10) Validacoes falhas / nao executadas

- Backend portable (`/health`, `/api/status`, `/api/produtos`): NAO EXECUTADO COM SUCESSO por ausencia de `fastapi/uvicorn` no Python do host atual.
- Teste E2E visual de zoom em navegador real (desktop/mobile): NAO EXECUTADO nesta rodada.

## 11) Itens movidos para quarentena

- Nesta rodada `v0.1.055`: sem novo movimento para quarentena.

## 12) Riscos e pendencias

- Sem dependencia Python correta, portable sobe apenas frontend.
- Ainda existem componentes legados `front_end/back_end` no DEV; migracao total para `app/frontend` e `app/backend` requer etapa dedicada para evitar quebra.
- Consolidacao final de imagens para `assets/images/produtos` ainda precisa fechamento completo com seed unica.

## 13) Proximo passo recomendado

1. Preparar runtime Python do portable com `fastapi` e `uvicorn` (sem instalar automaticamente pelo script).  
2. Executar teste real dos endpoints `8876` no portable.  
3. Fechar migracao de seed/imagens para fonte unica `data/seed` + `assets/images/produtos` em DEV e portable.  
4. Rodar teste manual de zoom (desktop/mobile) com evidencias de clique, ESC e fechamento por overlay.
