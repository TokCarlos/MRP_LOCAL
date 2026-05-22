# RELATORIO_BACKEND_PRODUTOS_v0.1.057

Data: 2026-05-22
Escopo: implementacao do primeiro backend real do modulo Produtos (SQLite + CRUD + fichas frontend), sem commit.

## Diagnostico inicial (obrigatorio, antes de alterar codigo)

### Estado inicial detectado
- Frontend ativo DEV detectado em `01-mrp/front_end` (SPA atual e paginas em uso).
- Backend ativo DEV detectado em `01-mrp/back_end/app` com FastAPI minimo (`/health`, `/api/status`, `/api/produtos`).
- Estrutura `01-mrp/app/frontend` e `01-mrp/app/backend` existe como alvo estrutural, mas nao e a fonte ativa principal nesta etapa.
- Backend atual de Produtos ainda usa seed/mock, sem banco SQLite, sem CRUD completo e sem fichas completas de cadastro/edicao no frontend.

### Arquivos alvo principais
- Backend:
  - `01-mrp/back_end/app/config.py`
  - `01-mrp/back_end/app/main.py`
  - `01-mrp/back_end/app/routes/produtos.py`
  - `01-mrp/back_end/app/services/produtos_service.py`
  - `01-mrp/back_end/app/repositories/produtos_repository.py`
  - novos modulos de persistencia SQLite/migrations/seed loader
- Frontend:
  - `01-mrp/front_end/pages/produtos_list.html`
  - `01-mrp/front_end/js/pages/produtos_list.js`
  - `01-mrp/front_end/css/pages/produtos_list.css`
- Sincronizacao de compatibilidade portable:
  - `portable/app/frontend/...` (JS/HTML/CSS de Produtos)
  - `portable/app/backend/...` (apenas o necessario para nao quebrar copia)

### Riscos iniciais
- Risco de quebrar o fluxo atual Produtos/BOM/Zoom ja corrigido.
- Risco de conflito com estado legado (`front_end/back_end` x `app/frontend/backend`).
- Risco de regressao visual se modais novos destoarem do padrao atual.
- Risco de dependencia de path fixo se persistencia nao usar resolver de paths existente.

### Decisoes tecnicas iniciais
1. Manter fonte ativa em `01-mrp/front_end` e `01-mrp/back_end` nesta etapa.
2. Implementar persistencia SQLite com caminho via resolver/config (sem hardcode de ambiente).
3. Preservar arquitetura `route -> service -> repository` e encapsular SQL fora de rotas.
4. Implementar CRUD logico (`ativo`) sem delete fisico.
5. Integrar frontend com API como fluxo principal e manter fallback controlado.
6. Sincronizar somente o necessario para portable nao ficar quebrado.

### O que sera alterado
- Camada backend de Produtos para incluir tabelas, repositorio SQLite, service de dominio, rotas CRUD de bases/produtos/bom.
- Configuracao de backend para raiz de banco e seed.
- Frontend Produtos para fichas/modais:
  - Nova Base ATA
  - Novo Produto
  - Editar Produto
  - Editar BOM
- Integracao frontend com novos endpoints.

### O que nao sera alterado
- `.git` e historico Git.
- Pasta proibida `C:\Users\carlo\Desktop\PCP SERVIDOR\PCP`.
- Implementacao de PostgreSQL, watchdog, instalador, autenticacao avancada, outros modulos.
- Reorganizacao profunda da arvore `01-mrp`.

---

## Execucao da implementacao
- Concluida nesta iteracao com backend SQLite + CRUD de Bases/Produtos/BOM e integracao frontend no modulo Produtos ativo.

## Entregas tecnicas

### Banco SQLite e persistencia
- Banco alvo configurado em `01-mrp/data/db/mrp_local_dev.sqlite` via `AppConfig`.
- Migration criada: `01-mrp/infrastructure/persistence/migrations/001_produtos.sql`.
- Tabelas criadas:
  - `produto_base_ata`
  - `produtos`
  - `produto_bom`
- Repositorio SQLite implementado com inicializacao idempotente de schema.

### Backend Produtos
- Camadas aplicadas: `route -> service -> repository -> database`.
- Novos modulos:
  - `01-mrp/back_end/app/domain/produtos_models.py`
  - `01-mrp/back_end/app/repositories/sqlite_db.py`
  - `01-mrp/back_end/app/core/normalize.py`
- Modulos alterados:
  - `01-mrp/back_end/app/config.py`
  - `01-mrp/back_end/app/repositories/produtos_repository.py`
  - `01-mrp/back_end/app/services/produtos_service.py`
  - `01-mrp/back_end/app/routes/produtos.py`
- Script de carga seed:
  - `03-vs/scripts/backend/seed_produtos_to_db.py`

### Endpoints implementados
- Bases:
  - `GET /api/produtos/bases`
  - `POST /api/produtos/bases`
  - `GET /api/produtos/bases/{id}`
  - `PUT /api/produtos/bases/{id}`
- Produtos:
  - `GET /api/produtos`
  - `GET /api/produtos/{id}`
  - `POST /api/produtos`
  - `PUT /api/produtos/{id}`
  - `PATCH /api/produtos/{id}/imagem`
  - `DELETE /api/produtos/{id}` (logico)
- BOM:
  - `GET /api/produtos/{id}/bom`
  - `POST /api/produtos/{id}/bom`
  - `PUT /api/produtos/{id}/bom`
  - `DELETE /api/produtos/{id}/bom/{bom_item_id}` (logico)

### Frontend Produtos (DEV ativo) e compatibilidade portable
- DEV alterado em:
  - `01-mrp/front_end/js/pages/produtos_list.js`
  - `01-mrp/front_end/pages/produtos_list.html`
  - `01-mrp/front_end/css/pages/produtos_list.css`
- Portable sincronizado com copia dos mesmos tres arquivos para:
  - `portable/app/frontend/js/pages/produtos_list.js`
  - `portable/app/frontend/pages/produtos_list.html`
  - `portable/app/frontend/css/pages/produtos_list.css`
- Fichas/modais implementados:
  - Nova Base ATA
  - Novo/Editar Produto
  - Editar BOM
- Fluxos ligados a API:
  - carregar produtos
  - criar base
  - criar/editar/inativar produto
  - carregar/editar BOM

### Regras aplicadas
- Validacao de empresa restrita a `jpl`, `aco`, `tcr`.
- `tcr` aceito como empresa, mas bloqueado para criacao de produtos nesta etapa.
- Produto exige Base ATA + item + nome oficial.
- `imagem_path` bloqueia caminhos absolutos/ambiente proibido.

## Validacoes executadas
- `git diff --check`: OK.
- `node --check`:
  - `01-mrp/front_end/js/pages/produtos_list.js`: OK.
  - `portable/app/frontend/js/pages/produtos_list.js`: OK.
- `python -m compileall` em backend ativo e script seed: OK.

## Validacoes pendentes/nao executadas
- Teste HTTP real dos endpoints (`/health`, `/api/status`, `/api/produtos`, `/api/produtos/bases`) nao executado no ambiente atual por ausencia de `fastapi` no runtime Python local.
- Teste manual completo de UI (modais CRUD/BOM/zoom) permanece pendente em execucao browser com backend levantado.

## Riscos e observacoes
- A integracao frontend foi ligada ao novo contrato `{ ok, data }`; qualquer cliente legado esperando `{ items }` precisa manter fallback.
- O backend depende de ambiente Python com FastAPI instalado para validacao fim-a-fim.
- Sem commit nesta entrega, conforme escopo.

## Correcoes complementares pos-validacao

### 1. UI Produtos quebrada apos implementacao CRUD

Causa:
- `init()` chamava funcoes inexistentes: `renderProdutos()`, `bindProdutosEvents()`, `bindImageZoom()`.
- Isso interrompia a inicializacao da tela Produtos e impedia clique, zoom e BOM.

Correcao:
- `init()` foi alinhado as funcoes reais existentes.
- Renderizacao passou a usar `renderProdutosFiltrados()`.
- Eventos passaram a ser inicializados por `initProdutosInteractions()`.
- Listeners criticos foram ajustados para comportamento idempotente.
- Parser da API passou a aceitar formatos compativeis:
  - `{ ok: true, data: [...] }`
  - `{ ok: true, data: { items: [...] } }`
  - `{ items: [...] }`

### 2. Erro de integracao frontend/backend por CORS

Causa:
- Frontend roda na porta `8765` e backend na porta `8876`.
- Browser bloqueava chamadas cross-origin em alguns fluxos.

Correcao:
- Backend recebeu configuracao CORS para DEV/local-first.
- Liberado acesso entre frontend `8765` e backend `8876`.

### 3. Erro "Failed to fetch" ao salvar BOM

Causa:
- Frontend chamava API fixa em `http://127.0.0.1:8876`.
- Quando o sistema era acessado por IP/hostname/Tailscale, o navegador tentava chamar `127.0.0.1` da maquina cliente, nao do servidor.

Correcao:
- Frontend passou a montar a URL da API usando o mesmo host da pagina atual e porta `8876`.
- Exemplo: `http://<host-da-pagina>:8876/api/produtos`.

### 4. Ativar/Inativar nao funcionava corretamente

Causa:
- Diferenca de tratamento entre boolean, `0/1` e strings de ativo.

Correcao:
- Frontend passou a normalizar ativo como boolean real antes de renderizar e enviar atualizacao.

### 5. Backend start usando Python errado

Causa:
- `mrp_backend_start.ps1` usava Python global, que nao tinha `fastapi`, `pydantic` e `uvicorn`.
- A venv correta estava em `01-mrp/runtime/venv_backend`.

Correcao:
- Script passou a priorizar `01-mrp/runtime/venv_backend/Scripts/python.exe`.
- Script passou a aguardar a porta `8876` por ate 15 segundos antes de declarar falha de LISTEN.
- Ordem de selecao registrada:
  1. `01-mrp/runtime/venv_backend/Scripts/python.exe`
  2. `python` do PATH
  3. `py` launcher
- Se as dependencias faltarem, o script orienta executar `03-vs/scripts/backend/setup_backend_dev_env.ps1`.
- Start oficial mantido com `python -m uvicorn app.main:app --host 0.0.0.0 --port 8876 --app-dir 01-mrp/back_end`.

### Arquivos relacionados
- `01-mrp/front_end/js/pages/produtos_list.js`
- `portable/app/frontend/js/pages/produtos_list.js`
- `01-mrp/back_end/app/main.py`
- `03-vs/scripts/servicos/mrp_backend_start.ps1`
- `01-mrp/back_end/requirements.txt`
- `03-vs/scripts/backend/setup_backend_dev_env.ps1`
- `03-vs/scripts/backend/test_backend_produtos_v0_1_057.py`

### Pendencias
- Testar manualmente Ativar/Inativar no navegador.
- Testar salvar BOM no navegador apos reiniciar backend.
- Validar CRUD completo pela UI.
- Validar portable depois, nao agora.
- Nao considerar homologado/blindado.

## Ajuste complementar do painel local DEV

- Painel local DEV passou a incluir controle operacional do backend na porta `8876`.
- Acoes adicionadas:
  - iniciar backend;
  - parar backend;
  - status backend;
  - healthcheck backend;
  - reiniciar backend.
- Scripts backend relacionados:
  - `03-vs/scripts/servicos/mrp_backend_start.ps1`
  - `03-vs/scripts/servicos/mrp_backend_stop.ps1`
  - `03-vs/scripts/servicos/mrp_backend_status.ps1`
  - `03-vs/scripts/servicos/mrp_backend_healthcheck.ps1`
- Painel tambem recebeu correcao de scroll geral e acionamento por Enter.
- Relatorio especifico: `03-vs/relatorios/RELATORIO_AJUSTE_PAINEL_BACKEND_v0.1.057.md`.
