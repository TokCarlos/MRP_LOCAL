from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    raise SystemExit(1)


def main() -> None:
    script_path = Path(__file__).resolve()
    project_root = script_path.parents[3]

    back_end_dir = project_root / "01-mrp" / "back_end"
    if str(back_end_dir) not in sys.path:
        sys.path.insert(0, str(back_end_dir))

    db_path = project_root / "01-mrp" / "data" / "db" / "mrp_local_dev.sqlite"
    seed_script = project_root / "03-vs" / "scripts" / "backend" / "seed_produtos_to_db.py"

    from app.main import app  # pylint: disable=import-outside-toplevel

    client = TestClient(app)

    endpoint_results = {}
    for endpoint in ["/health", "/api/status", "/api/produtos", "/api/produtos/bases"]:
        response = client.get(endpoint)
        endpoint_results[endpoint] = response.status_code
        if response.status_code != 200:
            fail(f"Endpoint {endpoint} retornou {response.status_code}")

    produtos_payload = client.get("/api/produtos").json()
    produtos = produtos_payload.get("data") or []
    if not produtos:
        fail("Endpoint /api/produtos retornou lista vazia.")
    first = produtos[0]
    for field in ["base_ata_id", "arp", "ata_numero", "empresa", "imagem_path"]:
        if first.get(field) in (None, ""):
            fail(f"Contrato da lista de produtos sem campo obrigatorio: {field}")

    if not db_path.exists():
        fail(f"Banco SQLite nao encontrado: {db_path}")

    with sqlite3.connect(db_path) as conn:
        table_names = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        required = {"produto_base_ata", "produtos", "produto_bom"}
        missing = sorted(required - table_names)
        if missing:
            fail(f"Tabelas ausentes no banco: {', '.join(missing)}")

        base_count = int(conn.execute("SELECT COUNT(*) FROM produto_base_ata").fetchone()[0])
        produtos_count = int(conn.execute("SELECT COUNT(*) FROM produtos WHERE ativo=1").fetchone()[0])

    if produtos_count == 0:
        if not seed_script.exists():
            fail("Banco sem produtos e script de seed nao encontrado.")
        run = subprocess.run([sys.executable, str(seed_script)], capture_output=True, text=True, check=False)
        if run.returncode != 0:
            fail(f"Seed falhou: {run.stderr.strip() or run.stdout.strip()}")
        with sqlite3.connect(db_path) as conn:
            base_count = int(conn.execute("SELECT COUNT(*) FROM produto_base_ata").fetchone()[0])
            produtos_count = int(conn.execute("SELECT COUNT(*) FROM produtos WHERE ativo=1").fetchone()[0])
        if produtos_count == 0:
            fail("Seed executado, mas produtos continuam zerados.")

    result = {
        "ok": True,
        "db_path": str(db_path),
        "bases_count": base_count,
        "produtos_count": produtos_count,
        "endpoints": endpoint_results,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
