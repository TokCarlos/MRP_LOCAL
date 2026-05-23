from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimePaths:
    mode: str
    root: Path
    app_root: Path
    frontend_root: Path
    backend_root: Path
    assets_root: Path
    data_root: Path
    seed_root: Path
    runtime_root: Path
    logs_root: Path
    tmp_root: Path


def _env_path(name: str) -> Path | None:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return None
    return Path(raw).expanduser().resolve()


def _detect_root(default_mode: str) -> tuple[str, Path]:
    env_root = _env_path("MRP_ROOT")
    env_mode = (os.getenv("MRP_MODE") or "").strip().lower()
    mode = env_mode if env_mode in {"dev", "portable"} else default_mode
    if env_root:
        return mode, env_root

    here = Path(__file__).resolve()
    parts = {p.name for p in here.parents}
    if "portable" in parts:
        for p in here.parents:
            if p.name == "portable":
                return "portable", p

    for p in here.parents:
        if (p / "01-mrp").exists() and (p / "portable").exists():
            return "dev", p
    return mode, here.parents[3]


def resolve_runtime_paths(default_mode: str = "dev") -> RuntimePaths:
    mode, root = _detect_root(default_mode=default_mode)
    app_root = _env_path("MRP_APP_ROOT") or (root / "app" if mode == "portable" else root / "01-mrp" / "app")
    default_frontend_root = app_root / "frontend" if mode == "portable" else root / "01-mrp" / "front_end"
    default_backend_root = app_root / "backend" if mode == "portable" else root / "01-mrp" / "back_end"
    frontend_root = _env_path("MRP_FRONTEND_ROOT") or default_frontend_root
    backend_root = _env_path("MRP_BACKEND_ROOT") or default_backend_root
    assets_root = _env_path("MRP_ASSETS_ROOT") or (root / "assets" if mode == "portable" else root / "01-mrp" / "assets")
    data_root = _env_path("MRP_DATA_ROOT") or (root / "data" if mode == "portable" else root / "01-mrp" / "data")
    seed_root = data_root / "seed"
    runtime_root = _env_path("MRP_RUNTIME_ROOT") or (root / "runtime" if mode == "portable" else root / "01-mrp" / "runtime")
    logs_root = _env_path("MRP_LOGS_ROOT") or (root / "logs" if mode == "portable" else root / "01-mrp" / "logs")
    tmp_root = _env_path("MRP_TMP_ROOT") or (root / "tmp" if mode == "portable" else root / "01-mrp" / "tmp")

    if not frontend_root.exists():
        raise RuntimeError(f"Frontend root ausente: {frontend_root}")
    if not backend_root.exists():
        raise RuntimeError(f"Backend root ausente: {backend_root}")
    if not seed_root.exists():
        raise RuntimeError(f"Seed root ausente: {seed_root}")

    return RuntimePaths(
        mode=mode,
        root=root,
        app_root=app_root,
        frontend_root=frontend_root,
        backend_root=backend_root,
        assets_root=assets_root,
        data_root=data_root,
        seed_root=seed_root,
        runtime_root=runtime_root,
        logs_root=logs_root,
        tmp_root=tmp_root,
    )
