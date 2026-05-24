from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from app.repositories.sqlite_db import get_connection, init_schema


class OrdensProducaoRepository:
    def __init__(self, db_path: Path, migration_path: Path) -> None:
        self._db_path = db_path
        self._migration_path = migration_path
        init_schema(self._db_path, self._migration_path)

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _conn(self):
        return get_connection(self._db_path)

    @staticmethod
    def _parse_json(value: Any) -> Any:
        if isinstance(value, str) and value.strip():
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return value

    def _history_row_to_dict(self, row: Any) -> Dict[str, Any]:
        item = dict(row)
        item["dados_antes"] = self._parse_json(item.get("dados_antes"))
        item["dados_depois"] = self._parse_json(item.get("dados_depois"))
        return item

    def gerar_proximo_numero_op(self, ano: int) -> Dict[str, Any]:
        now = self._now_iso()
        with self._conn() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT id, ultimo_seq FROM op_contadores WHERE ano = ?",
                (ano,),
            ).fetchone()
            counter_id: Optional[int] = None
            seq = 1
            if row:
                counter_id = int(row["id"])
                seq = int(row["ultimo_seq"] or 0) + 1
            aa = str(ano)[-2:]
            numero_op = f"{seq:03d}-{aa}"
            while conn.execute(
                "SELECT 1 FROM ordens_producao WHERE numero_op = ? LIMIT 1",
                (numero_op,),
            ).fetchone():
                seq += 1
                numero_op = f"{seq:03d}-{aa}"

            if counter_id is None:
                conn.execute(
                    """
                    INSERT INTO op_contadores (ano, ultimo_seq, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (ano, seq, now, now),
                )
            else:
                conn.execute(
                    "UPDATE op_contadores SET ultimo_seq = ?, updated_at = ? WHERE id = ?",
                    (seq, now, counter_id),
                )
            conn.commit()
        return {"ano": ano, "seq": seq, "numero_op": numero_op}

    def create_ordem(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO ordens_producao (
                    numero_op, ano, seq, rev,
                    empresa_key, empresa_nome, ata_key, ata_nome, numero_ata,
                    cliente, obra, modelo, tipo, material, solicitante,
                    data_entrega_tipo, data_entrega_data, data_entrega_valor,
                    status, observacoes, created_at, updated_at, created_by, ativo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    payload["numero_op"],
                    payload["ano"],
                    payload["seq"],
                    payload.get("rev") or "00",
                    payload["empresa_key"],
                    payload["empresa_nome"],
                    payload.get("ata_key"),
                    payload.get("ata_nome"),
                    payload.get("numero_ata"),
                    payload.get("cliente"),
                    payload.get("obra"),
                    payload.get("modelo"),
                    payload.get("tipo"),
                    payload.get("material"),
                    payload.get("solicitante"),
                    payload.get("data_entrega_tipo") or "TEXTO",
                    payload.get("data_entrega_data"),
                    payload.get("data_entrega_valor") or "NÃO DEFINIDO",
                    payload.get("status") or "RASCUNHO",
                    payload.get("observacoes"),
                    now,
                    now,
                    payload.get("created_by"),
                ),
            )
            op_id = int(cur.lastrowid)
            conn.commit()
        return self.get_ordem(op_id, include_inactive=True) or {}


    def create_ordem_completa(
        self,
        payload: Dict[str, Any],
        produtos_payloads: Iterable[Dict[str, Any]],
        processos: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Cria OP + produtos + BOM snapshot + processos + historico em uma unica transacao."""
        now = self._now_iso()
        ano = int(payload["ano"])
        processos_list = list(processos)
        produtos_list = list(produtos_payloads)
        with self._conn() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row_counter = conn.execute(
                "SELECT id, ultimo_seq FROM op_contadores WHERE ano = ?",
                (ano,),
            ).fetchone()
            counter_id: Optional[int] = None
            seq = 1
            if row_counter:
                counter_id = int(row_counter["id"])
                seq = int(row_counter["ultimo_seq"] or 0) + 1
            aa = str(ano)[-2:]
            numero_op = f"{seq:03d}-{aa}"
            while conn.execute("SELECT 1 FROM ordens_producao WHERE numero_op = ? LIMIT 1", (numero_op,)).fetchone():
                seq += 1
                numero_op = f"{seq:03d}-{aa}"

            if counter_id is None:
                conn.execute(
                    """
                    INSERT INTO op_contadores (ano, ultimo_seq, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (ano, seq, now, now),
                )
            else:
                conn.execute(
                    "UPDATE op_contadores SET ultimo_seq = ?, updated_at = ? WHERE id = ?",
                    (seq, now, counter_id),
                )

            cur_op = conn.execute(
                """
                INSERT INTO ordens_producao (
                    numero_op, ano, seq, rev,
                    empresa_key, empresa_nome, ata_key, ata_nome, numero_ata,
                    cliente, obra, modelo, tipo, material, solicitante,
                    data_entrega_tipo, data_entrega_data, data_entrega_valor,
                    status, observacoes, created_at, updated_at, created_by, ativo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    numero_op,
                    ano,
                    seq,
                    payload.get("rev") or "00",
                    payload.get("empresa_key") or "",
                    payload.get("empresa_nome") or "",
                    payload.get("ata_key"),
                    payload.get("ata_nome"),
                    payload.get("numero_ata"),
                    payload.get("cliente"),
                    payload.get("obra"),
                    payload.get("modelo"),
                    payload.get("tipo"),
                    payload.get("material"),
                    payload.get("solicitante"),
                    payload.get("data_entrega_tipo") or "TEXTO",
                    payload.get("data_entrega_data"),
                    payload.get("data_entrega_valor") or "NÃO DEFINIDO",
                    payload.get("status") or "RASCUNHO",
                    payload.get("observacoes"),
                    now,
                    now,
                    payload.get("created_by"),
                ),
            )
            op_id = int(cur_op.lastrowid)
            created_produtos: List[Dict[str, Any]] = []

            for ordem_item, item in enumerate(produtos_list, start=1):
                produto = item["produto"]
                quantidade = float(item.get("quantidade") or 0)
                cur_prod = conn.execute(
                    """
                    INSERT INTO ordem_producao_produtos (
                        op_id, produto_id, produto_key, item_ata, nome_produto, empresa_key, empresa_nome,
                        ata_key, ata_nome, numero_ata, imagem_path, quantidade, quantidade_inauguracao, material,
                        ordem_item, observacao, ativo, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                    """,
                    (
                        op_id,
                        int(produto["id"]),
                        produto.get("produto_key"),
                        produto.get("item_ata"),
                        produto.get("nome_oficial"),
                        produto.get("empresa_key"),
                        produto.get("empresa_nome"),
                        produto.get("ata_key"),
                        produto.get("ata_nome"),
                        produto.get("numero_ata"),
                        produto.get("imagem_path"),
                        quantidade,
                        item.get("quantidade_inauguracao"),
                        item.get("material"),
                        ordem_item,
                        item.get("observacao"),
                        now,
                        now,
                    ),
                )
                op_produto_id = int(cur_prod.lastrowid)
                created_produtos.append({"id": op_produto_id, "produto_id": int(produto["id"]), "quantidade": quantidade})

                for idx, bom in enumerate(item.get("bom_rows") or []):
                    quantidade_unitaria = float(bom.get("quantidade") or 0)
                    quantidade_total = quantidade_unitaria * quantidade
                    conn.execute(
                        """
                        INSERT INTO ordem_producao_bom (
                            op_id, op_produto_id, produto_id, bom_item_id_origem,
                            grupo, cod, material, dim1, dim2, espessura, revestimento, tamanho, unidade,
                            quantidade_unitaria, quantidade_produto, quantidade_total, ordem_item,
                            editado_manual, ativo, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1, ?, ?)
                        """,
                        (
                            op_id,
                            op_produto_id,
                            int(produto["id"]),
                            bom.get("id"),
                            bom.get("grupo"),
                            bom.get("cod"),
                            bom.get("material") or bom.get("item_nome"),
                            bom.get("dim1") or bom.get("observacao"),
                            bom.get("dim2"),
                            bom.get("espessura"),
                            bom.get("revestimento"),
                            bom.get("tamanho"),
                            bom.get("unidade"),
                            quantidade_unitaria,
                            quantidade,
                            quantidade_total,
                            int(bom.get("ordem_item") or (idx + 1)),
                            now,
                            now,
                        ),
                    )

                for processo in processos_list:
                    conn.execute(
                        """
                        INSERT INTO ordem_producao_processos (
                            op_id, op_produto_id, processo_key, processo_nome, ordem,
                            quantidade_planejada, quantidade_concluida, quantidade_falta,
                            status, observacao, ativo, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, 'PENDENTE', NULL, 1, ?, ?)
                        """,
                        (
                            op_id,
                            op_produto_id,
                            processo["processo_key"],
                            processo["processo_nome"],
                            int(processo["ordem"]),
                            quantidade,
                            quantidade,
                            now,
                            now,
                        ),
                    )

                detalhe_produto = f"Produto {produto.get('produto_key')} adicionado a OP na criação guiada."
                conn.execute(
                    """
                    INSERT INTO ordem_producao_historico (
                        op_id, entidade, entidade_id, acao, detalhe, dados_antes, dados_depois, created_at, created_by
                    ) VALUES (?, 'OP_PRODUTO', ?, 'PRODUTO_ADICIONADO', ?, NULL, ?, ?, ?)
                    """,
                    (
                        op_id,
                        op_produto_id,
                        detalhe_produto,
                        json.dumps({"produto_id": int(produto["id"]), "produto_key": produto.get("produto_key"), "quantidade": quantidade}, ensure_ascii=False, sort_keys=True),
                        now,
                        payload.get("created_by"),
                    ),
                )

            conn.execute(
                """
                INSERT INTO ordem_producao_historico (
                    op_id, entidade, entidade_id, acao, detalhe, dados_antes, dados_depois, created_at, created_by
                ) VALUES (?, 'OP', ?, 'OP_CRIADA', ?, NULL, ?, ?, ?)
                """,
                (
                    op_id,
                    op_id,
                    f"OP {numero_op} criada em fluxo guiado.",
                    json.dumps({"numero_op": numero_op, "status": payload.get("status") or "RASCUNHO", "produtos": created_produtos}, ensure_ascii=False, sort_keys=True),
                    now,
                    payload.get("created_by"),
                ),
            )
            conn.commit()
        return self.get_ordem(op_id, include_inactive=True) or {}

    def list_ordens(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        where_clause = "" if include_inactive else "WHERE o.ativo = 1"
        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT o.*,
                       COALESCE(px.total_produtos, 0) AS total_produtos,
                       COALESCE(px.total_unidades, 0) AS total_unidades
                FROM ordens_producao o
                LEFT JOIN (
                    SELECT op_id,
                           COUNT(*) AS total_produtos,
                           COALESCE(SUM(quantidade), 0) AS total_unidades
                    FROM ordem_producao_produtos
                    WHERE ativo = 1
                    GROUP BY op_id
                ) px ON px.op_id = o.id
                {where_clause}
                ORDER BY o.updated_at DESC, o.id DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def get_ordem(self, op_id: int, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        where_clause = "" if include_inactive else "AND o.ativo = 1"
        with self._conn() as conn:
            row = conn.execute(
                f"""
                SELECT o.*,
                       COALESCE(px.total_produtos, 0) AS total_produtos,
                       COALESCE(px.total_unidades, 0) AS total_unidades
                FROM ordens_producao o
                LEFT JOIN (
                    SELECT op_id,
                           COUNT(*) AS total_produtos,
                           COALESCE(SUM(quantidade), 0) AS total_unidades
                    FROM ordem_producao_produtos
                    WHERE ativo = 1
                    GROUP BY op_id
                ) px ON px.op_id = o.id
                WHERE o.id = ? {where_clause}
                """,
                (op_id,),
            ).fetchone()
        return dict(row) if row else None

    def update_ordem(self, op_id: int, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not fields:
            return self.get_ordem(op_id, include_inactive=True)
        now = self._now_iso()
        sets: List[str] = []
        values: List[Any] = []
        for key, value in fields.items():
            sets.append(f"{key} = ?")
            values.append(value)
        sets.append("updated_at = ?")
        values.append(now)
        values.append(op_id)

        with self._conn() as conn:
            conn.execute(
                f"UPDATE ordens_producao SET {', '.join(sets)} WHERE id = ?",
                tuple(values),
            )
            conn.commit()
        return self.get_ordem(op_id, include_inactive=True)

    def soft_delete_ordem(self, op_id: int) -> bool:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                """
                UPDATE ordens_producao
                SET ativo = 0, status = 'CANCELADA', updated_at = ?
                WHERE id = ? AND ativo = 1
                """,
                (now, op_id),
            )
            conn.commit()
        return int(cur.rowcount or 0) > 0

    def get_produto_snapshot(self, produto_id: int) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT p.id, p.produto_key, p.item_ata, p.nome_oficial, p.categoria, p.imagem_path, p.ativo,
                       b.empresa_key, b.empresa_nome, b.ata_key, b.ata_nome, b.numero_ata
                FROM produtos p
                INNER JOIN produto_base_ata b ON b.id = p.base_ata_id
                WHERE p.id = ?
                """,
                (produto_id,),
            ).fetchone()
        return dict(row) if row else None

    def list_produto_bom(self, produto_id: int) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT id, produto_id, grupo, cod, material, dim1, dim2, espessura, revestimento, tamanho,
                       unidade, quantidade, ordem_item, ativo
                FROM produto_bom
                WHERE produto_id = ? AND ativo = 1
                ORDER BY grupo, ordem_item, id
                """,
                (produto_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_op_produtos(self, op_id: int, include_inactive: bool = False) -> List[Dict[str, Any]]:
        where_clause = "" if include_inactive else "AND ativo = 1"
        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT *
                FROM ordem_producao_produtos
                WHERE op_id = ? {where_clause}
                ORDER BY ordem_item, id
                """,
                (op_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_op_produto(
        self, op_id: int, op_produto_id: int, include_inactive: bool = False
    ) -> Optional[Dict[str, Any]]:
        where_clause = "" if include_inactive else "AND ativo = 1"
        with self._conn() as conn:
            row = conn.execute(
                f"""
                SELECT *
                FROM ordem_producao_produtos
                WHERE op_id = ? AND id = ? {where_clause}
                """,
                (op_id, op_produto_id),
            ).fetchone()
        return dict(row) if row else None

    def create_op_produto(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO ordem_producao_produtos (
                    op_id, produto_id, produto_key, item_ata, nome_produto, empresa_key, empresa_nome,
                    ata_key, ata_nome, numero_ata, imagem_path, quantidade, quantidade_inauguracao, material,
                    ordem_item, observacao, ativo, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    payload["op_id"],
                    payload["produto_id"],
                    payload.get("produto_key"),
                    payload.get("item_ata"),
                    payload.get("nome_produto"),
                    payload.get("empresa_key"),
                    payload.get("empresa_nome"),
                    payload.get("ata_key"),
                    payload.get("ata_nome"),
                    payload.get("numero_ata"),
                    payload.get("imagem_path"),
                    float(payload.get("quantidade") or 0),
                    payload.get("quantidade_inauguracao"),
                    payload.get("material"),
                    int(payload.get("ordem_item") or 0),
                    payload.get("observacao"),
                    now,
                    now,
                ),
            )
            op_produto_id = int(cur.lastrowid)
            conn.commit()
        return self.get_op_produto(payload["op_id"], op_produto_id, include_inactive=True) or {}

    def update_op_produto(self, op_id: int, op_produto_id: int, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not fields:
            return self.get_op_produto(op_id, op_produto_id, include_inactive=True)
        now = self._now_iso()
        sets: List[str] = []
        values: List[Any] = []
        for key, value in fields.items():
            sets.append(f"{key} = ?")
            values.append(value)
        sets.append("updated_at = ?")
        values.append(now)
        values.extend([op_id, op_produto_id])
        with self._conn() as conn:
            conn.execute(
                f"UPDATE ordem_producao_produtos SET {', '.join(sets)} WHERE op_id = ? AND id = ?",
                tuple(values),
            )
            conn.commit()
        return self.get_op_produto(op_id, op_produto_id, include_inactive=True)

    def soft_delete_op_produto(self, op_id: int, op_produto_id: int) -> bool:
        now = self._now_iso()
        with self._conn() as conn:
            cur = conn.execute(
                """
                UPDATE ordem_producao_produtos
                SET ativo = 0, updated_at = ?
                WHERE op_id = ? AND id = ? AND ativo = 1
                """,
                (now, op_id, op_produto_id),
            )
            conn.commit()
        return int(cur.rowcount or 0) > 0

    def create_op_bom_from_snapshot(
        self,
        op_id: int,
        op_produto_id: int,
        produto_id: int,
        quantidade_produto: float,
        bom_rows: Iterable[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        now = self._now_iso()
        with self._conn() as conn:
            for idx, item in enumerate(bom_rows):
                quantidade_unitaria = float(item.get("quantidade") or 0)
                quantidade_total = quantidade_unitaria * float(quantidade_produto or 0)
                conn.execute(
                    """
                    INSERT INTO ordem_producao_bom (
                        op_id, op_produto_id, produto_id, bom_item_id_origem,
                        grupo, cod, material, dim1, dim2, espessura, revestimento, tamanho, unidade,
                        quantidade_unitaria, quantidade_produto, quantidade_total, ordem_item,
                        editado_manual, ativo, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 1, ?, ?)
                    """,
                    (
                        op_id,
                        op_produto_id,
                        produto_id,
                        item.get("id"),
                        item.get("grupo"),
                        item.get("cod"),
                        item.get("material") or item.get("item_nome"),
                        item.get("dim1") or item.get("observacao"),
                        item.get("dim2"),
                        item.get("espessura"),
                        item.get("revestimento"),
                        item.get("tamanho"),
                        item.get("unidade"),
                        quantidade_unitaria,
                        float(quantidade_produto or 0),
                        quantidade_total,
                        int(item.get("ordem_item") or (idx + 1)),
                        now,
                        now,
                    ),
                )
            conn.commit()
        return self.list_op_bom_by_produto(op_id, op_produto_id)

    def list_op_bom(self, op_id: int, include_inactive: bool = False) -> List[Dict[str, Any]]:
        where_clause = "" if include_inactive else "AND b.ativo = 1"
        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT b.*, p.nome_produto, p.ordem_item AS produto_ordem_item
                FROM ordem_producao_bom b
                INNER JOIN ordem_producao_produtos p ON p.id = b.op_produto_id
                WHERE b.op_id = ? {where_clause}
                ORDER BY p.ordem_item, b.op_produto_id, b.grupo, b.ordem_item, b.id
                """,
                (op_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_op_bom_by_produto(self, op_id: int, op_produto_id: int) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM ordem_producao_bom
                WHERE op_id = ? AND op_produto_id = ? AND ativo = 1
                ORDER BY grupo, ordem_item, id
                """,
                (op_id, op_produto_id),
            ).fetchall()
        return [dict(row) for row in rows]

    def recalc_bom_quantidades(self, op_id: int, op_produto_id: int, quantidade_produto: float) -> None:
        now = self._now_iso()
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE ordem_producao_bom
                SET quantidade_produto = ?,
                    quantidade_total = quantidade_unitaria * ?,
                    updated_at = ?
                WHERE op_id = ? AND op_produto_id = ? AND ativo = 1
                """,
                (float(quantidade_produto or 0), float(quantidade_produto or 0), now, op_id, op_produto_id),
            )
            conn.commit()

    def update_op_bom_items(self, op_id: int, itens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        now = self._now_iso()
        with self._conn() as conn:
            for item in itens:
                bom_id = int(item["id"])
                current = conn.execute(
                    """
                    SELECT id, quantidade_unitaria, quantidade_produto
                    FROM ordem_producao_bom
                    WHERE id = ? AND op_id = ? AND ativo = 1
                    """,
                    (bom_id, op_id),
                ).fetchone()
                if not current:
                    continue
                sets: List[str] = []
                values: List[Any] = []
                for key in ("cod", "material", "dim1", "dim2", "espessura", "revestimento", "tamanho", "unidade", "ordem_item"):
                    if key in item:
                        sets.append(f"{key} = ?")
                        values.append(item.get(key))

                quantidade_unitaria = float(current["quantidade_unitaria"] or 0)
                quantidade_produto = float(current["quantidade_produto"] or 0)
                if "quantidade_unitaria" in item and item.get("quantidade_unitaria") is not None:
                    quantidade_unitaria = float(item["quantidade_unitaria"])
                    sets.append("quantidade_unitaria = ?")
                    values.append(quantidade_unitaria)
                if "quantidade_produto" in item and item.get("quantidade_produto") is not None:
                    quantidade_produto = float(item["quantidade_produto"])
                    sets.append("quantidade_produto = ?")
                    values.append(quantidade_produto)

                quantidade_total = quantidade_unitaria * quantidade_produto
                sets.extend(["quantidade_total = ?", "editado_manual = 1", "updated_at = ?"])
                values.extend([quantidade_total, now])
                values.extend([bom_id, op_id])
                conn.execute(
                    f"UPDATE ordem_producao_bom SET {', '.join(sets)} WHERE id = ? AND op_id = ?",
                    tuple(values),
                )
            conn.commit()
        return self.list_op_bom(op_id)

    def soft_delete_op_bom_by_produto(self, op_id: int, op_produto_id: int) -> None:
        now = self._now_iso()
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE ordem_producao_bom
                SET ativo = 0, updated_at = ?
                WHERE op_id = ? AND op_produto_id = ? AND ativo = 1
                """,
                (now, op_id, op_produto_id),
            )
            conn.commit()

    def create_processos_padrao(
        self,
        op_id: int,
        op_produto_id: int,
        quantidade_planejada: float,
        processos: Iterable[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        now = self._now_iso()
        with self._conn() as conn:
            for item in processos:
                planejada = float(quantidade_planejada or 0)
                conn.execute(
                    """
                    INSERT INTO ordem_producao_processos (
                        op_id, op_produto_id, processo_key, processo_nome, ordem,
                        quantidade_planejada, quantidade_concluida, quantidade_falta,
                        status, observacao, ativo, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, 'PENDENTE', NULL, 1, ?, ?)
                    """,
                    (
                        op_id,
                        op_produto_id,
                        item["processo_key"],
                        item["processo_nome"],
                        int(item["ordem"]),
                        planejada,
                        planejada,
                        now,
                        now,
                    ),
                )
            conn.commit()
        return self.list_processos_by_produto(op_id, op_produto_id)

    def list_processos(self, op_id: int, include_inactive: bool = False) -> List[Dict[str, Any]]:
        where_clause = "" if include_inactive else "AND p.ativo = 1"
        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT p.*, op.nome_produto, op.ordem_item AS produto_ordem_item
                FROM ordem_producao_processos p
                INNER JOIN ordem_producao_produtos op ON op.id = p.op_produto_id
                WHERE p.op_id = ? {where_clause}
                ORDER BY op.ordem_item, p.op_produto_id, p.ordem, p.id
                """,
                (op_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_processos_all_ordens(self) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT p.*, op.numero_op, op.cliente, op.obra, op.empresa_nome,
                       op.data_entrega_tipo, op.data_entrega_data, op.data_entrega_valor,
                       op.status AS status_op, op.updated_at AS op_updated_at
                FROM ordem_producao_processos p
                INNER JOIN ordem_producao_produtos pp
                    ON pp.id = p.op_produto_id
                   AND pp.ativo = 1
                INNER JOIN ordens_producao op
                    ON op.id = p.op_id
                   AND op.ativo = 1
                WHERE p.ativo = 1
                ORDER BY p.op_id, p.ordem, p.id
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def list_processos_by_produto(self, op_id: int, op_produto_id: int) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM ordem_producao_processos
                WHERE op_id = ? AND op_produto_id = ? AND ativo = 1
                ORDER BY ordem, id
                """,
                (op_id, op_produto_id),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_processo(self, op_id: int, processo_id: int) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM ordem_producao_processos
                WHERE op_id = ? AND id = ? AND ativo = 1
                """,
                (op_id, processo_id),
            ).fetchone()
        return dict(row) if row else None

    def recalc_processos_planejamento(self, op_id: int, op_produto_id: int, quantidade_planejada: float) -> None:
        now = self._now_iso()
        planejada = float(quantidade_planejada or 0)
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT id, quantidade_concluida
                FROM ordem_producao_processos
                WHERE op_id = ? AND op_produto_id = ? AND ativo = 1
                """,
                (op_id, op_produto_id),
            ).fetchall()
            for row in rows:
                concluida = float(row["quantidade_concluida"] or 0)
                falta = max(planejada - concluida, 0)
                conn.execute(
                    """
                    UPDATE ordem_producao_processos
                    SET quantidade_planejada = ?, quantidade_falta = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (planejada, falta, now, int(row["id"])),
                )
            conn.commit()

    def update_processo(self, op_id: int, processo_id: int, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        current = self.get_processo(op_id, processo_id)
        if not current:
            return None
        now = self._now_iso()
        quantidade_planejada = float(current.get("quantidade_planejada") or 0)
        quantidade_concluida = float(current.get("quantidade_concluida") or 0)

        sets: List[str] = []
        values: List[Any] = []
        if "quantidade_concluida" in fields and fields["quantidade_concluida"] is not None:
            quantidade_concluida = float(fields["quantidade_concluida"])
            sets.append("quantidade_concluida = ?")
            values.append(quantidade_concluida)
        if "status" in fields and fields["status"] is not None:
            sets.append("status = ?")
            values.append(fields["status"])
        if "observacao" in fields:
            sets.append("observacao = ?")
            values.append(fields.get("observacao"))

        quantidade_falta = max(quantidade_planejada - quantidade_concluida, 0)
        sets.extend(["quantidade_falta = ?", "updated_at = ?"])
        values.extend([quantidade_falta, now, op_id, processo_id])

        with self._conn() as conn:
            conn.execute(
                f"UPDATE ordem_producao_processos SET {', '.join(sets)} WHERE op_id = ? AND id = ?",
                tuple(values),
            )
            conn.commit()
        return self.get_processo(op_id, processo_id)

    def soft_delete_processos_by_produto(self, op_id: int, op_produto_id: int) -> None:
        now = self._now_iso()
        with self._conn() as conn:
            conn.execute(
                """
                UPDATE ordem_producao_processos
                SET ativo = 0, updated_at = ?
                WHERE op_id = ? AND op_produto_id = ? AND ativo = 1
                """,
                (now, op_id, op_produto_id),
            )
            conn.commit()

    def registrar_historico(
        self,
        op_id: int,
        entidade: Optional[str],
        entidade_id: Optional[int],
        acao: str,
        detalhe: Optional[str],
        dados_antes: Optional[Dict[str, Any]] = None,
        dados_depois: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        now = self._now_iso()
        dados_antes_raw = json.dumps(dados_antes, ensure_ascii=False, sort_keys=True) if dados_antes is not None else None
        dados_depois_raw = json.dumps(dados_depois, ensure_ascii=False, sort_keys=True) if dados_depois is not None else None
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO ordem_producao_historico (
                    op_id, entidade, entidade_id, acao, detalhe, dados_antes, dados_depois, created_at, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (op_id, entidade, entidade_id, acao, detalhe, dados_antes_raw, dados_depois_raw, now, created_by),
            )
            history_id = int(cur.lastrowid)
            row = conn.execute(
                """
                SELECT *
                FROM ordem_producao_historico
                WHERE id = ?
                """,
                (history_id,),
            ).fetchone()
            conn.commit()
        return self._history_row_to_dict(row) if row else {}

    def list_historico(self, op_id: int) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM ordem_producao_historico
                WHERE op_id = ?
                ORDER BY id DESC
                """,
                (op_id,),
            ).fetchall()
        return [self._history_row_to_dict(row) for row in rows]
