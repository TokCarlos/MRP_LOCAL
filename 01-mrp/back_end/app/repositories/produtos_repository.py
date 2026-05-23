from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.normalize import EMPRESA_NOME_BY_KEY
from app.domain.produto import Produto
from app.repositories.sqlite_db import get_connection, init_schema


class ProdutosRepository:
    def __init__(self, db_path: Path, migration_path: Path) -> None:
        self._db_path = db_path
        self._migration_path = migration_path
        init_schema(self._db_path, self._migration_path)

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _conn(self):
        return get_connection(self._db_path)

    def list_produtos(self, include_inactive: bool = False) -> List[Produto]:
        where_clause = "" if include_inactive else "WHERE p.ativo = 1"
        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT p.id, p.base_ata_id, p.produto_key, p.item_ata, p.nome_oficial, p.categoria, p.imagem_path,
                       p.ativo, p.created_at, p.updated_at,
                       b.ata_nome, b.ata_key, b.numero_ata, b.empresa_key, b.empresa_nome
                FROM produtos p
                INNER JOIN produto_base_ata b ON b.id = p.base_ata_id
                {where_clause}
                ORDER BY p.id
                """
            ).fetchall()
        out: List[Produto] = []
        for row in rows:
            raw = dict(row)
            raw["categoria_key"] = raw.get("categoria")
            out.append(Produto.from_seed(raw))
        return out

    def list_bases(self) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT id, ata_nome, ata_key, numero_ata, empresa_key, empresa_nome, ativo, created_at, updated_at
                FROM produto_base_ata
                ORDER BY id
                """
            ).fetchall()
        return [dict(r) for r in rows]

    def get_base(self, base_id: int) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT id, ata_nome, ata_key, numero_ata, empresa_key, empresa_nome, ativo, created_at, updated_at
                FROM produto_base_ata WHERE id = ?
                """,
                (base_id,),
            ).fetchone()
        return dict(row) if row else None

    def create_base(self, ata_nome: str, ata_key: str, numero_ata: str, empresa_key: str) -> Dict[str, Any]:
        now = self._now_iso()
        empresa_nome = EMPRESA_NOME_BY_KEY[empresa_key]
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO produto_base_ata (
                    ata_nome, ata_key, numero_ata, empresa_key, empresa_nome, ativo, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (ata_nome, ata_key, numero_ata, empresa_key, empresa_nome, now, now),
            )
            base_id = int(cur.lastrowid)
            conn.commit()
        return self.get_base(base_id) or {}

    def update_base(
        self, base_id: int, ata_nome: str, ata_key: str, numero_ata: str, empresa_key: str, ativo: bool
    ) -> Optional[Dict[str, Any]]:
        now = self._now_iso()
        empresa_nome = EMPRESA_NOME_BY_KEY[empresa_key]
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE produto_base_ata
                SET ata_nome = ?, ata_key = ?, numero_ata = ?, empresa_key = ?, empresa_nome = ?, ativo = ?, updated_at = ?
                WHERE id = ?
                """,
                (ata_nome, ata_key, numero_ata, empresa_key, empresa_nome, 1 if ativo else 0, now, base_id),
            )
            conn.commit()
        return self.get_base(base_id)

    def get_produto(self, produto_id: int) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT p.id, p.base_ata_id, p.produto_key, p.item_ata, p.nome_oficial, p.categoria, p.imagem_path,
                       p.ativo, p.created_at, p.updated_at,
                       b.ata_nome, b.ata_key, b.numero_ata, b.empresa_key, b.empresa_nome
                FROM produtos p
                INNER JOIN produto_base_ata b ON b.id = p.base_ata_id
                WHERE p.id = ?
                """,
                (produto_id,),
            ).fetchone()
        return dict(row) if row else None

    def create_produto(
        self,
        base_ata_id: int,
        produto_key: str,
        item_ata: str,
        nome_oficial: str,
        categoria: Optional[str],
        imagem_path: Optional[str],
    ) -> Dict[str, Any]:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO produtos (
                    base_ata_id, produto_key, item_ata, nome_oficial, categoria, imagem_path, ativo, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (base_ata_id, produto_key, item_ata, nome_oficial, categoria, imagem_path, now, now),
            )
            produto_id = int(cur.lastrowid)
            conn.commit()
        return self.get_produto(produto_id) or {}

    def update_produto(
        self,
        produto_id: int,
        base_ata_id: int,
        item_ata: str,
        nome_oficial: str,
        categoria: Optional[str],
        imagem_path: Optional[str],
        ativo: bool,
    ) -> Optional[Dict[str, Any]]:
        now = self._now_iso()
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE produtos
                SET base_ata_id = ?, item_ata = ?, nome_oficial = ?, categoria = ?, imagem_path = ?, ativo = ?, updated_at = ?
                WHERE id = ?
                """,
                (base_ata_id, item_ata, nome_oficial, categoria, imagem_path, 1 if ativo else 0, now, produto_id),
            )
            conn.commit()
        return self.get_produto(produto_id)

    def patch_imagem(self, produto_id: int, imagem_path: Optional[str]) -> Optional[Dict[str, Any]]:
        now = self._now_iso()
        with self._conn() as conn:
            conn.execute(
                "UPDATE produtos SET imagem_path = ?, updated_at = ? WHERE id = ?",
                (imagem_path, now, produto_id),
            )
            conn.commit()
        return self.get_produto(produto_id)

    def soft_delete_produto(self, produto_id: int) -> bool:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE produtos SET ativo = 0, updated_at = ? WHERE id = ?",
                (now, produto_id),
            )
            conn.commit()
        return cur.rowcount > 0

    def _history_row_to_dict(self, row) -> Dict[str, Any]:
        item = dict(row)
        for key in ("dados_antes", "dados_depois"):
            raw = item.get(key)
            if isinstance(raw, str) and raw.strip():
                try:
                    item[key] = json.loads(raw)
                except json.JSONDecodeError:
                    pass
        return item

    def list_bom_historico(self, produto_id: int) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT id, produto_id, bom_item_id, acao, grupo, cod, material,
                       dados_antes, dados_depois, detalhe, created_at, created_by, ativo
                FROM produto_bom_historico
                WHERE produto_id = ? AND ativo = 1
                ORDER BY id DESC
                """,
                (produto_id,),
            ).fetchall()
        return [self._history_row_to_dict(row) for row in rows]

    def get_bom_ultima_atualizacao(self, produto_id: int) -> Optional[str]:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT created_at
                FROM produto_bom_historico
                WHERE produto_id = ? AND ativo = 1
                ORDER BY id DESC
                LIMIT 1
                """,
                (produto_id,),
            ).fetchone()
        return str(row["created_at"]) if row else None

    def add_bom_history_event(
        self,
        produto_id: int,
        acao: str,
        grupo: Optional[str] = None,
        cod: Optional[str] = None,
        material: Optional[str] = None,
        bom_item_id: Optional[int] = None,
        dados_antes: Optional[Dict[str, Any]] = None,
        dados_depois: Optional[Dict[str, Any]] = None,
        detalhe: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        now = self._now_iso()
        before_json = json.dumps(dados_antes, ensure_ascii=False, sort_keys=True) if dados_antes is not None else None
        after_json = json.dumps(dados_depois, ensure_ascii=False, sort_keys=True) if dados_depois is not None else None
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO produto_bom_historico (
                    produto_id, bom_item_id, acao, grupo, cod, material,
                    dados_antes, dados_depois, detalhe, created_at, created_by, ativo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    produto_id,
                    bom_item_id,
                    acao,
                    grupo,
                    cod,
                    material,
                    before_json,
                    after_json,
                    detalhe,
                    now,
                    created_by,
                ),
            )
            history_id = int(cur.lastrowid)
            row = conn.execute(
                """
                SELECT id, produto_id, bom_item_id, acao, grupo, cod, material,
                       dados_antes, dados_depois, detalhe, created_at, created_by, ativo
                FROM produto_bom_historico
                WHERE id = ?
                """,
                (history_id,),
            ).fetchone()
            conn.commit()
        return self._history_row_to_dict(row) if row else {}

    def add_bom_history_events(self, produto_id: int, events: List[Dict[str, Any]]) -> None:
        for event in events:
            self.add_bom_history_event(produto_id=produto_id, **event)

    def clear_bom_history(self, produto_id: int, created_by: Optional[str] = None) -> Dict[str, Any]:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE produto_bom_historico SET ativo = 0 WHERE produto_id = ? AND ativo = 1",
                (produto_id,),
            )
            deleted = int(cur.rowcount or 0)
            conn.execute(
                """
                INSERT INTO produto_bom_historico (
                    produto_id, bom_item_id, acao, grupo, cod, material,
                    dados_antes, dados_depois, detalhe, created_at, created_by, ativo
                )
                VALUES (?, NULL, 'HISTORICO_LIMPO', NULL, NULL, NULL, NULL, NULL, ?, ?, ?, 1)
                """,
                (produto_id, f"Histórico da BOM limpo. Eventos anteriores arquivados: {deleted}", now, created_by),
            )
            conn.commit()
        return {"produto_id": produto_id, "eventos_arquivados": deleted, "ultima_atualizacao_bom": now}

    def list_bom(self, produto_id: int) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT id, produto_id, grupo,
                       cod, material, dim1, dim2, espessura, revestimento, tamanho,
                       quantidade, unidade,
                       item_nome, observacao, ordem_item, ativo, created_at, updated_at
                FROM produto_bom
                WHERE produto_id = ? AND ativo = 1
                ORDER BY grupo, ordem_item, id
                """,
                (produto_id,),
            ).fetchall()
        out: List[Dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            # Compatibilidade para registros anteriores a estrutura nova.
            if not item.get("material"):
                item["material"] = item.get("item_nome")
            if not item.get("dim1"):
                item["dim1"] = item.get("observacao")
            out.append(item)
        return out

    def add_bom_item(
        self,
        produto_id: int,
        grupo: str,
        cod: Optional[str],
        material: str,
        dim1: Optional[str],
        dim2: Optional[str],
        espessura: Optional[str],
        revestimento: Optional[str],
        tamanho: Optional[str],
        quantidade: Optional[float],
        unidade: Optional[str],
        item_nome: str,
        observacao: Optional[str],
        ordem_item: Optional[int],
    ) -> Dict[str, Any]:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO produto_bom (
                    produto_id, grupo, cod, material, dim1, dim2, espessura, revestimento, tamanho,
                    quantidade, unidade, item_nome, observacao, ordem_item, ativo, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    produto_id,
                    grupo,
                    cod,
                    material,
                    dim1,
                    dim2,
                    espessura,
                    revestimento,
                    tamanho,
                    quantidade,
                    unidade,
                    item_nome,
                    observacao,
                    ordem_item,
                    now,
                    now,
                ),
            )
            bom_id = int(cur.lastrowid)
            row = conn.execute(
                """
                SELECT id, produto_id, grupo,
                       cod, material, dim1, dim2, espessura, revestimento, tamanho,
                       quantidade, unidade,
                       item_nome, observacao, ordem_item, ativo, created_at, updated_at
                FROM produto_bom WHERE id = ?
                """,
                (bom_id,),
            ).fetchone()
            conn.commit()
        return dict(row) if row else {}

    def replace_bom(self, produto_id: int, itens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        now = self._now_iso()
        with self._conn() as conn:
            conn.execute(
                "UPDATE produto_bom SET ativo = 0, updated_at = ? WHERE produto_id = ? AND ativo = 1",
                (now, produto_id),
            )
            for idx, item in enumerate(itens):
                conn.execute(
                    """
                    INSERT INTO produto_bom (
                        produto_id, grupo, cod, material, dim1, dim2, espessura, revestimento, tamanho,
                        quantidade, unidade, item_nome, observacao, ordem_item, ativo, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                    """,
                    (
                        produto_id,
                        item["grupo"],
                        item.get("cod"),
                        item.get("material"),
                        item.get("dim1"),
                        item.get("dim2"),
                        item.get("espessura"),
                        item.get("revestimento"),
                        item.get("tamanho"),
                        item.get("quantidade"),
                        item.get("unidade"),
                        item.get("item_nome") or item.get("material"),
                        item.get("observacao") or item.get("dim1"),
                        item.get("ordem") if item.get("ordem") is not None else idx + 1,
                        now,
                        now,
                    ),
                )
            conn.commit()
        return self.list_bom(produto_id)

    def delete_bom_item(self, produto_id: int, bom_item_id: int) -> bool:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                """
                UPDATE produto_bom
                SET ativo = 0, updated_at = ?
                WHERE id = ? AND produto_id = ?
                """,
                (now, bom_item_id, produto_id),
            )
            conn.commit()
        return cur.rowcount > 0
