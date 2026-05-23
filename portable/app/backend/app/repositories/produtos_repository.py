from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.adapters.produtos_seed_adapter import ProdutosSeedAdapter
from app.domain.produto import Produto


class ProdutosRepository:
    def __init__(
        self,
        adapter: ProdutosSeedAdapter,
        bom_path: Optional[Path] = None,
        bom_historico_path: Optional[Path] = None,
        imagem_state_path: Optional[Path] = None,
    ) -> None:
        self._adapter = adapter
        self._bom_path = bom_path
        self._bom_historico_path = bom_historico_path
        self._imagem_state_path = imagem_state_path

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _load_imagem_state(self) -> Dict[str, Any]:
        if not self._imagem_state_path or not self._imagem_state_path.exists():
            return {}
        try:
            data = json.loads(self._imagem_state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return data if isinstance(data, dict) else {}

    def _save_imagem_state(self, data: Dict[str, Any]) -> None:
        if not self._imagem_state_path:
            return
        self._imagem_state_path.parent.mkdir(parents=True, exist_ok=True)
        self._imagem_state_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _merge_imagem_state(self, row: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(row)
        keys = []
        if row.get("id") is not None:
            keys.append(f"id:{row.get('id')}")
        if row.get("produto_key"):
            keys.append(f"key:{row.get('produto_key')}")
        for key in keys:
            imagem_path = state.get(key)
            if isinstance(imagem_path, str) and imagem_path.strip():
                out["imagem_path"] = imagem_path.strip()
                out["imagem"] = {"preview": imagem_path.strip()}
                break
        return out

    def list_produtos(self) -> List[Produto]:
        rows = self._adapter.load_produtos()
        state = self._load_imagem_state()
        return [Produto.from_seed(self._merge_imagem_state(row, state)) for row in rows]

    def get_produto(self, produto_id: int) -> Optional[Produto]:
        for produto in self.list_produtos():
            if produto.id == produto_id:
                return produto
        return None

    def patch_imagem(self, produto_id: int, imagem_path: Optional[str]) -> Optional[Produto]:
        produto = self.get_produto(produto_id)
        if not produto:
            return None
        state = self._load_imagem_state()
        value = (imagem_path or "").strip() or None
        state[f"id:{produto_id}"] = value
        if produto.produto_key:
            state[f"key:{produto.produto_key}"] = value
        self._save_imagem_state(state)
        return self.get_produto(produto_id)

    def _load_bom_rows(self) -> List[Dict[str, Any]]:
        if not self._bom_path or not self._bom_path.exists():
            return []
        try:
            data = json.loads(self._bom_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        return [row for row in data if isinstance(row, dict)]

    def _save_bom_rows(self, rows: List[Dict[str, Any]]) -> None:
        if not self._bom_path:
            return
        self._bom_path.parent.mkdir(parents=True, exist_ok=True)
        self._bom_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_history_rows(self) -> List[Dict[str, Any]]:
        if not self._bom_historico_path or not self._bom_historico_path.exists():
            return []
        try:
            data = json.loads(self._bom_historico_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        if not isinstance(data, list):
            return []
        return [row for row in data if isinstance(row, dict)]

    def _save_history_rows(self, rows: List[Dict[str, Any]]) -> None:
        if not self._bom_historico_path:
            return
        self._bom_historico_path.parent.mkdir(parents=True, exist_ok=True)
        self._bom_historico_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_bom_historico(self, produto_id: int) -> List[Dict[str, Any]]:
        rows = [
            row
            for row in self._load_history_rows()
            if int(row.get("produto_id") or 0) == produto_id and bool(row.get("ativo", True))
        ]
        return sorted(rows, key=lambda r: int(r.get("id") or 0), reverse=True)

    def get_bom_ultima_atualizacao(self, produto_id: int) -> Optional[str]:
        rows = self.list_bom_historico(produto_id)
        return str(rows[0].get("created_at")) if rows else None

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
        rows = self._load_history_rows()
        now = self._now_iso()
        next_id = max([int(row.get("id") or 0) for row in rows] or [0]) + 1
        row: Dict[str, Any] = {
            "id": next_id,
            "produto_id": produto_id,
            "bom_item_id": bom_item_id,
            "acao": acao,
            "grupo": grupo,
            "cod": cod,
            "material": material,
            "dados_antes": dados_antes,
            "dados_depois": dados_depois,
            "detalhe": detalhe,
            "created_at": now,
            "created_by": created_by,
            "ativo": True,
        }
        rows.append(row)
        self._save_history_rows(rows)
        return row

    def add_bom_history_events(self, produto_id: int, events: List[Dict[str, Any]]) -> None:
        for event in events:
            self.add_bom_history_event(produto_id=produto_id, **event)

    def clear_bom_history(self, produto_id: int, created_by: Optional[str] = None) -> Dict[str, Any]:
        rows = self._load_history_rows()
        now = self._now_iso()
        deleted = 0
        for row in rows:
            if int(row.get("produto_id") or 0) == produto_id and bool(row.get("ativo", True)):
                row["ativo"] = False
                deleted += 1
        next_id = max([int(row.get("id") or 0) for row in rows] or [0]) + 1
        rows.append({
            "id": next_id,
            "produto_id": produto_id,
            "bom_item_id": None,
            "acao": "HISTORICO_LIMPO",
            "grupo": None,
            "cod": None,
            "material": None,
            "dados_antes": None,
            "dados_depois": None,
            "detalhe": f"Histórico da BOM limpo. Eventos anteriores arquivados: {deleted}",
            "created_at": now,
            "created_by": created_by,
            "ativo": True,
        })
        self._save_history_rows(rows)
        return {"produto_id": produto_id, "eventos_arquivados": deleted, "ultima_atualizacao_bom": now}

    @staticmethod
    def _normalize_read_item(item: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(item)
        if not out.get("material"):
            out["material"] = out.get("item_nome")
        if not out.get("dim1"):
            out["dim1"] = out.get("observacao")
        return out

    def list_bom(self, produto_id: int) -> List[Dict[str, Any]]:
        rows = [
            self._normalize_read_item(row)
            for row in self._load_bom_rows()
            if int(row.get("produto_id") or 0) == produto_id and bool(row.get("ativo", True))
        ]
        return sorted(rows, key=lambda r: (str(r.get("grupo") or ""), int(r.get("ordem_item") or 0), int(r.get("id") or 0)))

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
        rows = self._load_bom_rows()
        now = self._now_iso()
        next_id = max([int(row.get("id") or 0) for row in rows] or [0]) + 1
        row: Dict[str, Any] = {
            "id": next_id,
            "produto_id": produto_id,
            "grupo": grupo,
            "cod": cod,
            "material": material,
            "dim1": dim1,
            "dim2": dim2,
            "espessura": espessura,
            "revestimento": revestimento,
            "tamanho": tamanho,
            "quantidade": quantidade,
            "unidade": unidade,
            "item_nome": item_nome,
            "observacao": observacao,
            "ordem_item": ordem_item,
            "ativo": True,
            "created_at": now,
            "updated_at": now,
        }
        rows.append(row)
        self._save_bom_rows(rows)
        return row

    def replace_bom(self, produto_id: int, itens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rows = self._load_bom_rows()
        now = self._now_iso()
        for row in rows:
            if int(row.get("produto_id") or 0) == produto_id and bool(row.get("ativo", True)):
                row["ativo"] = False
                row["updated_at"] = now
        next_id = max([int(row.get("id") or 0) for row in rows] or [0]) + 1
        for idx, item in enumerate(itens):
            rows.append({
                "id": next_id,
                "produto_id": produto_id,
                "grupo": item["grupo"],
                "cod": item.get("cod"),
                "material": item.get("material"),
                "dim1": item.get("dim1"),
                "dim2": item.get("dim2"),
                "espessura": item.get("espessura"),
                "revestimento": item.get("revestimento"),
                "tamanho": item.get("tamanho"),
                "quantidade": item.get("quantidade"),
                "unidade": item.get("unidade"),
                "item_nome": item.get("item_nome") or item.get("material"),
                "observacao": item.get("observacao") or item.get("dim1"),
                "ordem_item": item.get("ordem") if item.get("ordem") is not None else idx + 1,
                "ativo": True,
                "created_at": now,
                "updated_at": now,
            })
            next_id += 1
        self._save_bom_rows(rows)
        return self.list_bom(produto_id)

    def delete_bom_item(self, produto_id: int, bom_item_id: int) -> bool:
        rows = self._load_bom_rows()
        now = self._now_iso()
        changed = False
        for row in rows:
            if int(row.get("id") or 0) == bom_item_id and int(row.get("produto_id") or 0) == produto_id:
                row["ativo"] = False
                row["updated_at"] = now
                changed = True
                break
        if changed:
            self._save_bom_rows(rows)
        return changed
