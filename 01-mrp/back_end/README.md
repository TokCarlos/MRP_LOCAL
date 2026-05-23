# back_end

Backend oficial atual do MRP_LOCAL.

## Estado atual

- Backend ativo: `01-mrp/back_end`.
- Framework: FastAPI.
- Porta DEV: `8876`.
- Primeiro dominio real: Produtos.
- Banco DEV/runtime: `01-mrp/data/db/mrp_local_dev.sqlite` quando gerado.
- Upload de imagens de usuario: `01-mrp/data/media/produtos`.
- Midia runtime servida por `/media/produtos/...`.

## Regras

- Nao usar caminho absoluto de usuario como regra de negocio.
- Usar resolver/configuracao do projeto.
- Nao versionar banco SQLite runtime, logs, venv ou cache.
- `01-mrp/app/backend` nao deve rodar como backend ativo nesta fase.
- Produtos deve seguir camadas: routes -> services -> repositories -> database.

## Endpoints minimos validados

- `GET /health`
- `GET /api/status`
- `GET /api/produtos`
- `GET /api/produtos/bases`

## Setup DEV

Criar/validar venv:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\backend\setup_backend_dev_env.ps1
```

Iniciar backend:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_backend_start.ps1
```
