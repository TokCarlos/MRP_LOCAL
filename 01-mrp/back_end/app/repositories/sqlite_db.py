from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable


PRODUTO_BOM_COLUMNS: tuple[tuple[str, str], ...] = (
    ("cod", "TEXT"),
    ("material", "TEXT"),
    ("dim1", "TEXT"),
    ("dim2", "TEXT"),
    ("espessura", "TEXT"),
    ("revestimento", "TEXT"),
    ("tamanho", "TEXT"),
)


def get_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _existing_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows: Iterable[sqlite3.Row] = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {str(row[1]) for row in rows}


def _ensure_produto_bom_columns(conn: sqlite3.Connection) -> None:
    if not _table_exists(conn, "produto_bom"):
        return
    existing = _existing_columns(conn, "produto_bom")
    for column_name, column_type in PRODUTO_BOM_COLUMNS:
        if column_name not in existing:
            conn.execute(f"ALTER TABLE produto_bom ADD COLUMN {column_name} {column_type}")



def _normalize_produtos_core_data(conn: sqlite3.Connection) -> None:
    if _table_exists(conn, "produto_base_ata"):
        conn.execute("""
            UPDATE produto_base_ata
            SET empresa_key = 'aco'
            WHERE lower(empresa_key) IN ('aco', 'ao') OR empresa_key IN ('AÇO', 'Aço', 'aço')
        """)
        conn.execute("""
            UPDATE produto_base_ata
            SET empresa_nome = 'Aço'
            WHERE empresa_key = 'aco'
        """)
        conn.execute("""
            UPDATE produto_base_ata
            SET empresa_key = lower(empresa_key)
            WHERE lower(empresa_key) IN ('jpl', 'tcr')
        """)

    if _table_exists(conn, "produtos"):
        collisions = conn.execute("""
            SELECT lower(produto_key) AS key_norm, COUNT(*) AS total
            FROM produtos
            GROUP BY lower(produto_key)
            HAVING total > 1
        """).fetchall()
        if not collisions:
            conn.execute("UPDATE produtos SET produto_key = lower(produto_key)")

def init_schema(db_path: Path, migration_path: Path) -> None:
    sql = migration_path.read_text(encoding="utf-8")
    with get_connection(db_path) as conn:
        conn.executescript(sql)
        _ensure_produto_bom_columns(conn)
        _normalize_produtos_core_data(conn)
        conn.commit()
