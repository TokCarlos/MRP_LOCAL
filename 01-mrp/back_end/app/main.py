from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import load_config
from app.routes import health, ordens_producao, produtos, status

cfg = load_config()
app = FastAPI(title="MRP Backend", version=cfg.version)
cfg.media_root.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    # DEV/local-first: frontend pode ser aberto por localhost, IP LAN, Tailscale ou hostname.
    # Sem credenciais; liberar origem evita falha de preflight em PUT/PATCH/DELETE do CRUD.
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.build_router(cfg))
app.include_router(status.build_router(cfg))
app.include_router(produtos.build_router(cfg))
app.include_router(ordens_producao.build_router(cfg))
app.mount("/media", StaticFiles(directory=str(cfg.media_root)), name="media")
