from __future__ import annotations

from typing import Dict

from app.config import AppConfig


def build_status_contract(cfg: AppConfig) -> Dict[str, object]:
    return {
        "ok": True,
        "service": "mrp_backend",
        "version": cfg.version,
        "environment": cfg.environment,
        "host": cfg.host,
        "port": cfg.port,
        "project_root": str(cfg.project_root),
        "backend_root": str(cfg.backend_root),
        "data_source": str(cfg.produtos_seed_path),
    }

