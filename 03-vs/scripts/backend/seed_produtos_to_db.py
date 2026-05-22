from __future__ import annotations

import json
import sys
from pathlib import Path


def _load_paths_module(repo_root: Path):
    path = repo_root / "01-mrp" / "infrastructure" / "config" / "paths.py"
    if not path.exists():
        return None
    import importlib.util

    spec = importlib.util.spec_from_file_location("mrp_paths", path)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    back_end_dir = repo_root / "01-mrp" / "back_end"
    if str(back_end_dir) not in sys.path:
        sys.path.insert(0, str(back_end_dir))
    mod = _load_paths_module(repo_root)
    if mod:
        resolved = mod.resolve_runtime_paths(default_mode="dev")
        data_root = resolved.data_root
    else:
        data_root = repo_root / "01-mrp" / "data"

    seed_path = data_root / "seed" / "produtos_seed.json"
    if not seed_path.exists():
        legacy_seed = repo_root / "01-mrp" / "front_end" / "data" / "produtos_seed.json"
        if legacy_seed.exists():
            seed_path = legacy_seed
    db_path = data_root / "db" / "mrp_local_dev.sqlite"
    migration_path = repo_root / "01-mrp" / "infrastructure" / "persistence" / "migrations" / "001_produtos.sql"

    if not seed_path.exists():
        print(f"[ERRO] seed ausente: {seed_path}")
        return 1

    from app.repositories.produtos_repository import ProdutosRepository
    from app.services.produtos_service import ProdutosService

    repo = ProdutosRepository(db_path=db_path, migration_path=migration_path)
    svc = ProdutosService(repository=repo, image_root=repo_root / "01-mrp" / "front_end", seed_path=seed_path)
    svc.bootstrap_seed_if_needed()

    payload = {"ok": True, "seed": str(seed_path), "db": str(db_path), "count": len(repo.list_produtos())}
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
