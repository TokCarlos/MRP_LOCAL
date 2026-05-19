#!/usr/bin/env python3
"""
MRP_LOCAL - Setup de credencial administrativa local.
Cria/atualiza 01-mrp/config/local/admin_auth.local.json com hash PBKDF2-HMAC-SHA256.
"""

from __future__ import annotations

import getpass
import hashlib
import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path


def resolve_repo_root() -> Path:
    # 03-vs/scripts/painel -> subir 3 niveis
    return Path(__file__).resolve().parents[3]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def pbkdf2_hash(password: str, salt_bytes: bytes, iterations: int) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt_bytes,
        iterations,
    )
    return digest.hex()


def write_json_utf8(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    repo_root = resolve_repo_root()
    local_dir = repo_root / "01-mrp" / "config" / "local"
    output_file = local_dir / "admin_auth.local.json"

    print("MRP_LOCAL - Setup de Credencial Admin Local")
    print(f"Repositorio: {repo_root}")
    print(f"Arquivo local: {output_file}")
    print("Este arquivo nao deve ser versionado no Git.")

    pw1 = getpass.getpass("Defina o PIN/senha administrativa local: ").strip()
    if len(pw1) < 6:
        print("ERRO: use pelo menos 6 caracteres.")
        return 1

    pw2 = getpass.getpass("Confirme o PIN/senha administrativa local: ").strip()
    if pw1 != pw2:
        print("ERRO: confirmacao diferente.")
        return 1

    iterations = 260_000
    salt_bytes = secrets.token_bytes(16)
    payload = {
        "version": "v0.1.049",
        "auth_type": "pbkdf2-hmac-sha256",
        "password_hash": pbkdf2_hash(pw1, salt_bytes, iterations),
        "salt": salt_bytes.hex(),
        "iterations": iterations,
        "created_at": utc_now_iso(),
        "note": "Arquivo local administrativo. Nao versionar.",
    }

    write_json_utf8(output_file, payload)
    try:
        # Tenta restringir permissao no Windows para o usuario atual.
        os.chmod(output_file, 0o600)
    except OSError:
        pass

    print("OK: credencial administrativa local criada/atualizada.")
    print("Ajuste permissao do arquivo para acesso apenas do administrador local.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

