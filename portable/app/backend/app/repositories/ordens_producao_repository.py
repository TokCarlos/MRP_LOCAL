from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class OrdensProducaoRepository:
    TABLES = (
        "op_contadores",
        "ordens_producao",
        "ordem_producao_produtos",
        "ordem_producao_bom",
        "ordem_producao_processos",
        "ordem_producao_historico",
    )

    def __init__(self, runtime_path: Path) -> None:
        self._runtime_path = runtime_path
        self._runtime_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_runtime()

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _ensure_runtime(self) -> None:
        if self._runtime_path.exists():
            return
        self._save({name: [] for name in self.TABLES})

    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            raw = json.loads(self._runtime_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            raw = {}
        if not isinstance(raw, dict):
            raw = {}
        for name in self.TABLES:
            if not isinstance(raw.get(name), list):
                raw[name] = []
        return raw

    def _save(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        self._runtime_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _next_id(rows: List[Dict[str, Any]]) -> int:
        return max([int(row.get("id") or 0) for row in rows] or [0]) + 1

    @staticmethod
    def _to_float(value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def gerar_proximo_numero_op(self, ano: int) -> Dict[str, Any]:
        db = self._load()
        counters = db["op_contadores"]
        now = self._now_iso()
        counter = next((item for item in counters if int(item.get("ano") or 0) == ano), None)
        if counter is None:
            counter = {
                "id": self._next_id(counters),
                "ano": ano,
                "ultimo_seq": 0,
                "created_at": now,
                "updated_at": now,
            }
            counters.append(counter)
        counter["ultimo_seq"] = int(counter.get("ultimo_seq") or 0) + 1
        counter["updated_at"] = now
        seq = int(counter["ultimo_seq"])
        numero_op = f"{seq:03d}-{str(ano)[-2:]}"
        self._save(db)
        return {"ano": ano, "seq": seq, "numero_op": numero_op}

    def create_ordem(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        db = self._load()
        rows = db["ordens_producao"]
        now = self._now_iso()
        row = {
            "id": self._next_id(rows),
            "numero_op": payload["numero_op"],
            "ano": payload["ano"],
            "seq": payload["seq"],
            "rev": payload.get("rev") or "00",
            "empresa_key": payload.get("empresa_key") or "",
            "empresa_nome": payload.get("empresa_nome") or "",
            "ata_key": payload.get("ata_key"),
            "ata_nome": payload.get("ata_nome"),
            "numero_ata": payload.get("numero_ata"),
            "cliente": payload.get("cliente"),
            "obra": payload.get("obra"),
            "modelo": payload.get("modelo"),
            "tipo": payload.get("tipo"),
            "material": payload.get("material"),
            "solicitante": payload.get("solicitante"),
            "data_entrega_tipo": payload.get("data_entrega_tipo") or "TEXTO",
            "data_entrega_data": payload.get("data_entrega_data"),
            "data_entrega_valor": payload.get("data_entrega_valor") or "NÃO DEFINIDO",
            "status": payload.get("status") or "RASCUNHO",
            "observacoes": payload.get("observacoes"),
            "created_at": now,
            "updated_at": now,
            "created_by": payload.get("created_by"),
            "ativo": 1,
        }
        rows.append(row)
        self._save(db)
        return row

    def list_ordens(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        db = self._load()
        ordens = db["ordens_producao"]
        produtos = db["ordem_producao_produtos"]
        out: List[Dict[str, Any]] = []
        for row in ordens:
            if not include_inactive and int(row.get("ativo") or 0) != 1:
                continue
            op_id = int(row.get("id") or 0)
            op_produtos = [item for item in produtos if int(item.get("op_id") or 0) == op_id and int(item.get("ativo") or 0) == 1]
            total_unidades = sum(self._to_float(item.get("quantidade"), 0) for item in op_produtos)
            merged = dict(row)
            merged["total_produtos"] = len(op_produtos)
            merged["total_unidades"] = total_unidades
            out.append(merged)
        return sorted(out, key=lambda item: str(item.get("updated_at") or ""), reverse=True)

    def get_ordem(self, op_id: int, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        for row in self.list_ordens(include_inactive=True):
            if int(row.get("id") or 0) == op_id:
                if not include_inactive and int(row.get("ativo") or 0) != 1:
                    return None
                return row
        return None

    def update_ordem(self, op_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = self._load()
        rows = db["ordens_producao"]
        target = next((row for row in rows if int(row.get("id") or 0) == op_id), None)
        if not target:
            return None
        for key, value in updates.items():
            target[key] = value
        target["updated_at"] = self._now_iso()
        self._save(db)
        return self.get_ordem(op_id, include_inactive=True)

    def soft_delete_ordem(self, op_id: int) -> bool:
        updated = self.update_ordem(op_id, {"ativo": 0, "status": "CANCELADA"})
        return updated is not None

    def list_op_produtos(self, op_id: int, include_inactive: bool = False) -> List[Dict[str, Any]]:
        db = self._load()
        rows = [row for row in db["ordem_producao_produtos"] if int(row.get("op_id") or 0) == op_id]
        if not include_inactive:
            rows = [row for row in rows if int(row.get("ativo") or 0) == 1]
        return sorted(rows, key=lambda item: (int(item.get("ordem_item") or 0), int(item.get("id") or 0)))

    def get_op_produto(self, op_id: int, op_produto_id: int, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        rows = self.list_op_produtos(op_id, include_inactive=True)
        row = next((item for item in rows if int(item.get("id") or 0) == op_produto_id), None)
        if not row:
            return None
        if not include_inactive and int(row.get("ativo") or 0) != 1:
            return None
        return row

    def create_op_produto(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        db = self._load()
        rows = db["ordem_producao_produtos"]
        now = self._now_iso()
        row = {
            "id": self._next_id(rows),
            "op_id": payload["op_id"],
            "produto_id": payload["produto_id"],
            "produto_key": payload.get("produto_key"),
            "item_ata": payload.get("item_ata"),
            "nome_produto": payload.get("nome_produto"),
            "empresa_key": payload.get("empresa_key"),
            "empresa_nome": payload.get("empresa_nome"),
            "ata_key": payload.get("ata_key"),
            "ata_nome": payload.get("ata_nome"),
            "numero_ata": payload.get("numero_ata"),
            "imagem_path": payload.get("imagem_path"),
            "quantidade": self._to_float(payload.get("quantidade"), 0.0),
            "quantidade_inauguracao": payload.get("quantidade_inauguracao"),
            "material": payload.get("material"),
            "ordem_item": int(payload.get("ordem_item") or 0),
            "observacao": payload.get("observacao"),
            "ativo": 1,
            "created_at": now,
            "updated_at": now,
        }
        rows.append(row)
        self._save(db)
        return row

    def update_op_produto(self, op_id: int, op_produto_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = self._load()
        rows = db["ordem_producao_produtos"]
        row = next((item for item in rows if int(item.get("op_id") or 0) == op_id and int(item.get("id") or 0) == op_produto_id), None)
        if not row:
            return None
        for key, value in updates.items():
            row[key] = value
        row["updated_at"] = self._now_iso()
        self._save(db)
        return row

    def soft_delete_op_produto(self, op_id: int, op_produto_id: int) -> bool:
        row = self.update_op_produto(op_id, op_produto_id, {"ativo": 0})
        return row is not None

    def list_op_bom(self, op_id: int, include_inactive: bool = False) -> List[Dict[str, Any]]:
        db = self._load()
        rows = [row for row in db["ordem_producao_bom"] if int(row.get("op_id") or 0) == op_id]
        if not include_inactive:
            rows = [row for row in rows if int(row.get("ativo") or 0) == 1]
        return sorted(rows, key=lambda item: (int(item.get("op_produto_id") or 0), int(item.get("ordem_item") or 0), int(item.get("id") or 0)))

    def list_op_bom_by_produto(self, op_id: int, op_produto_id: int) -> List[Dict[str, Any]]:
        return [
            row
            for row in self.list_op_bom(op_id, include_inactive=False)
            if int(row.get("op_produto_id") or 0) == op_produto_id
        ]

    def create_op_bom_from_snapshot(
        self,
        op_id: int,
        op_produto_id: int,
        produto_id: int,
        quantidade_produto: float,
        bom_rows: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        db = self._load()
        rows = db["ordem_producao_bom"]
        now = self._now_iso()
        for idx, item in enumerate(bom_rows):
            quantidade_unitaria = self._to_float(item.get("quantidade"), 0.0)
            quantidade_total = quantidade_unitaria * self._to_float(quantidade_produto, 0.0)
            rows.append(
                {
                    "id": self._next_id(rows),
                    "op_id": op_id,
                    "op_produto_id": op_produto_id,
                    "produto_id": produto_id,
                    "bom_item_id_origem": item.get("id"),
                    "grupo": item.get("grupo"),
                    "cod": item.get("cod"),
                    "material": item.get("material") or item.get("item_nome"),
                    "dim1": item.get("dim1") or item.get("observacao"),
                    "dim2": item.get("dim2"),
                    "espessura": item.get("espessura"),
                    "revestimento": item.get("revestimento"),
                    "tamanho": item.get("tamanho"),
                    "unidade": item.get("unidade"),
                    "quantidade_unitaria": quantidade_unitaria,
                    "quantidade_produto": self._to_float(quantidade_produto, 0.0),
                    "quantidade_total": quantidade_total,
                    "ordem_item": int(item.get("ordem_item") or (idx + 1)),
                    "editado_manual": 0,
                    "ativo": 1,
                    "created_at": now,
                    "updated_at": now,
                }
            )
        self._save(db)
        return self.list_op_bom_by_produto(op_id, op_produto_id)

    def recalc_bom_quantidades(self, op_id: int, op_produto_id: int, quantidade_produto: float) -> None:
        db = self._load()
        rows = db["ordem_producao_bom"]
        now = self._now_iso()
        for row in rows:
            if int(row.get("op_id") or 0) != op_id or int(row.get("op_produto_id") or 0) != op_produto_id or int(row.get("ativo") or 0) != 1:
                continue
            row["quantidade_produto"] = self._to_float(quantidade_produto, 0.0)
            row["quantidade_total"] = self._to_float(row.get("quantidade_unitaria"), 0.0) * self._to_float(quantidade_produto, 0.0)
            row["updated_at"] = now
        self._save(db)

    def update_op_bom_items(self, op_id: int, itens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        db = self._load()
        rows = db["ordem_producao_bom"]
        now = self._now_iso()
        for item in itens:
            bom_id = int(item.get("id") or 0)
            row = next((r for r in rows if int(r.get("id") or 0) == bom_id and int(r.get("op_id") or 0) == op_id and int(r.get("ativo") or 0) == 1), None)
            if not row:
                continue
            for key in ("cod", "material", "dim1", "dim2", "espessura", "revestimento", "tamanho", "unidade", "ordem_item"):
                if key in item:
                    row[key] = item.get(key)
            if "quantidade_unitaria" in item and item.get("quantidade_unitaria") is not None:
                row["quantidade_unitaria"] = self._to_float(item.get("quantidade_unitaria"), 0.0)
            row["quantidade_total"] = self._to_float(row.get("quantidade_unitaria"), 0.0) * self._to_float(row.get("quantidade_produto"), 0.0)
            row["editado_manual"] = 1
            row["updated_at"] = now
        self._save(db)
        return self.list_op_bom(op_id, include_inactive=False)

    def soft_delete_op_bom_by_produto(self, op_id: int, op_produto_id: int) -> None:
        db = self._load()
        now = self._now_iso()
        for row in db["ordem_producao_bom"]:
            if int(row.get("op_id") or 0) == op_id and int(row.get("op_produto_id") or 0) == op_produto_id and int(row.get("ativo") or 0) == 1:
                row["ativo"] = 0
                row["updated_at"] = now
        self._save(db)

    def create_processos_padrao(self, op_id: int, op_produto_id: int, quantidade_planejada: float, processos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        db = self._load()
        rows = db["ordem_producao_processos"]
        now = self._now_iso()
        planejada = self._to_float(quantidade_planejada, 0.0)
        for item in processos:
            rows.append(
                {
                    "id": self._next_id(rows),
                    "op_id": op_id,
                    "op_produto_id": op_produto_id,
                    "processo_key": item.get("processo_key"),
                    "processo_nome": item.get("processo_nome"),
                    "ordem": int(item.get("ordem") or 0),
                    "quantidade_planejada": planejada,
                    "quantidade_concluida": 0.0,
                    "quantidade_falta": planejada,
                    "status": "PENDENTE",
                    "observacao": None,
                    "ativo": 1,
                    "created_at": now,
                    "updated_at": now,
                }
            )
        self._save(db)
        return self.list_processos_by_produto(op_id, op_produto_id)

    def list_processos(self, op_id: int, include_inactive: bool = False) -> List[Dict[str, Any]]:
        db = self._load()
        rows = [row for row in db["ordem_producao_processos"] if int(row.get("op_id") or 0) == op_id]
        if not include_inactive:
            rows = [row for row in rows if int(row.get("ativo") or 0) == 1]
        return sorted(rows, key=lambda item: (int(item.get("op_produto_id") or 0), int(item.get("ordem") or 0), int(item.get("id") or 0)))

    def list_processos_by_produto(self, op_id: int, op_produto_id: int) -> List[Dict[str, Any]]:
        return [
            row
            for row in self.list_processos(op_id, include_inactive=False)
            if int(row.get("op_produto_id") or 0) == op_produto_id
        ]

    def get_processo(self, op_id: int, processo_id: int) -> Optional[Dict[str, Any]]:
        rows = self.list_processos(op_id, include_inactive=True)
        row = next((item for item in rows if int(item.get("id") or 0) == processo_id), None)
        if not row or int(row.get("ativo") or 0) != 1:
            return None
        return row

    def recalc_processos_planejamento(self, op_id: int, op_produto_id: int, quantidade_planejada: float) -> None:
        db = self._load()
        now = self._now_iso()
        planejada = self._to_float(quantidade_planejada, 0.0)
        for row in db["ordem_producao_processos"]:
            if int(row.get("op_id") or 0) != op_id or int(row.get("op_produto_id") or 0) != op_produto_id or int(row.get("ativo") or 0) != 1:
                continue
            concluida = self._to_float(row.get("quantidade_concluida"), 0.0)
            row["quantidade_planejada"] = planejada
            row["quantidade_falta"] = max(planejada - concluida, 0)
            row["updated_at"] = now
        self._save(db)

    def update_processo(self, op_id: int, processo_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = self._load()
        rows = db["ordem_producao_processos"]
        row = next((item for item in rows if int(item.get("op_id") or 0) == op_id and int(item.get("id") or 0) == processo_id and int(item.get("ativo") or 0) == 1), None)
        if not row:
            return None
        if "quantidade_concluida" in updates and updates.get("quantidade_concluida") is not None:
            row["quantidade_concluida"] = self._to_float(updates.get("quantidade_concluida"), 0.0)
        if "status" in updates and updates.get("status") is not None:
            row["status"] = updates.get("status")
        if "observacao" in updates:
            row["observacao"] = updates.get("observacao")
        row["quantidade_falta"] = max(self._to_float(row.get("quantidade_planejada"), 0.0) - self._to_float(row.get("quantidade_concluida"), 0.0), 0.0)
        row["updated_at"] = self._now_iso()
        self._save(db)
        return row

    def soft_delete_processos_by_produto(self, op_id: int, op_produto_id: int) -> None:
        db = self._load()
        now = self._now_iso()
        for row in db["ordem_producao_processos"]:
            if int(row.get("op_id") or 0) == op_id and int(row.get("op_produto_id") or 0) == op_produto_id and int(row.get("ativo") or 0) == 1:
                row["ativo"] = 0
                row["updated_at"] = now
        self._save(db)

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
        db = self._load()
        rows = db["ordem_producao_historico"]
        row = {
            "id": self._next_id(rows),
            "op_id": op_id,
            "entidade": entidade,
            "entidade_id": entidade_id,
            "acao": acao,
            "detalhe": detalhe,
            "dados_antes": dados_antes,
            "dados_depois": dados_depois,
            "created_at": self._now_iso(),
            "created_by": created_by,
        }
        rows.append(row)
        self._save(db)
        return row

    def list_historico(self, op_id: int) -> List[Dict[str, Any]]:
        db = self._load()
        rows = [row for row in db["ordem_producao_historico"] if int(row.get("op_id") or 0) == op_id]
        return sorted(rows, key=lambda item: int(item.get("id") or 0), reverse=True)
