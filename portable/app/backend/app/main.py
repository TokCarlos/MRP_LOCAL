from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import load_config
from app.routes import health, produtos, status

cfg = load_config()
app = FastAPI(title="MRP Backend", version=cfg.version)
cfg.media_root.mkdir(parents=True, exist_ok=True)

app.include_router(health.build_router(cfg))
app.include_router(status.build_router(cfg))
app.include_router(produtos.build_router(cfg))
app.mount("/media", StaticFiles(directory=str(cfg.media_root)), name="media")

