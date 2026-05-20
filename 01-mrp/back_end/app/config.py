from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    version: str
    environment: str
    host: str
    port: int
    project_root: Path
    backend_root: Path
    produtos_seed_path: Path
    produtos_image_root: Path


def _resolve_project_root() -> Path:
    # .../01-mrp/back_end/app/config.py -> project root
    return Path(__file__).resolve().parents[3]


def load_config() -> AppConfig:
    project_root = _resolve_project_root()
    backend_root = project_root / "01-mrp" / "back_end"
    seed_path = project_root / "01-mrp" / "front_end" / "data" / "produtos_seed.json"
    image_root = project_root / "01-mrp" / "front_end"

    host = (os.getenv("MRP_BACKEND_HOST") or "127.0.0.1").strip() or "127.0.0.1"
    port_raw = (os.getenv("MRP_BACKEND_PORT") or "8876").strip() or "8876"
    env = (os.getenv("MRP_BACKEND_ENV") or "dev").strip() or "dev"

    try:
        port = int(port_raw)
    except ValueError:
        port = 8876

    return AppConfig(
        version="v0.1.053b",
        environment=env,
        host=host,
        port=port,
        project_root=project_root,
        backend_root=backend_root,
        produtos_seed_path=seed_path,
        produtos_image_root=image_root,
    )

