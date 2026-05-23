from __future__ import annotations

import os
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
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
    produtos_bom_path: Path
    produtos_bom_historico_path: Path
    media_root: Path
    produtos_upload_root: Path
    produtos_upload_public_prefix: str
    produtos_imagem_state_path: Path


def _resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_paths_module(project_root: Path):
    candidates = [
        project_root / "infrastructure" / "config" / "paths.py",
        project_root / "01-mrp" / "infrastructure" / "config" / "paths.py",
    ]
    for candidate in candidates:
        if candidate.exists():
            spec = spec_from_file_location("mrp_paths", candidate)
            if spec and spec.loader:
                module = module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
    return None


def load_config() -> AppConfig:
    project_root = _resolve_project_root()
    paths_module = _load_paths_module(project_root)

    backend_root = project_root / "app" / "backend"
    seed_path = project_root / "data" / "seed" / "produtos_seed.json"
    image_root = project_root / "app" / "frontend"
    bom_path = project_root / "runtime" / "produtos_bom.json"
    bom_historico_path = project_root / "runtime" / "produtos_bom_historico.json"
    media_root = project_root / "runtime" / "media"
    upload_root = media_root / "produtos"
    upload_public_prefix = "media/produtos"
    imagem_state_path = project_root / "runtime" / "produtos_imagens.json"

    if paths_module:
        resolved = paths_module.resolve_runtime_paths(default_mode="portable")
        backend_root = resolved.backend_root
        preferred_seed = resolved.seed_root / "produtos_seed.json"
        fallback_seed = resolved.frontend_root / "data" / "produtos_seed.json"
        seed_path = preferred_seed if preferred_seed.exists() else fallback_seed
        image_root = resolved.frontend_root
        bom_path = resolved.runtime_root / "produtos_bom.json"
        bom_historico_path = resolved.runtime_root / "produtos_bom_historico.json"
        media_root = resolved.runtime_root / "media"
        upload_root = media_root / "produtos"
        upload_public_prefix = "media/produtos"
        imagem_state_path = resolved.runtime_root / "produtos_imagens.json"

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
        produtos_bom_path=bom_path,
        produtos_bom_historico_path=bom_historico_path,
        media_root=media_root,
        produtos_upload_root=upload_root,
        produtos_upload_public_prefix=upload_public_prefix,
        produtos_imagem_state_path=imagem_state_path,
    )
