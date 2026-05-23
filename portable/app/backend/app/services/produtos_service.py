from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
import unicodedata
from typing import Any, Dict, List, Optional, Set, Tuple

from app.core.paths import normalize_rel_path
from app.domain.produto import Produto
from app.domain.produtos_models import BomItemInput
from app.repositories.produtos_repository import ProdutosRepository


@dataclass
class ProdutosValidationReport:
    total_produtos: int = 0
    empresas: Set[str] = field(default_factory=set)
    atas: Set[str] = field(default_factory=set)
    categorias: Set[str] = field(default_factory=set)
    produtos_sem_imagem: List[str] = field(default_factory=list)
    imagens_inexistentes: List[str] = field(default_factory=list)
    duplicidades_produto_key: List[str] = field(default_factory=list)
    duplicidades_item_empresa_ata: List[str] = field(default_factory=list)
    alertas: List[str] = field(default_factory=list)
    erros: List[str] = field(default_factory=list)


class ProdutosService:
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
    IMAGE_MAX_BYTES = 5 * 1024 * 1024

    def __init__(
        self,
        repository: ProdutosRepository,
        image_root: Path,
        upload_root: Optional[Path] = None,
        upload_public_prefix: str = "media/produtos",
    ) -> None:
        self._repository = repository
        self._image_root = image_root
        self._upload_root = upload_root or (image_root / "runtime" / "media" / "produtos")
        self._upload_public_prefix = upload_public_prefix.strip("/\\")

    def list_produtos(self) -> List[Produto]:
        return self._repository.list_produtos()

    def get_produto(self, produto_id: int) -> Produto:
        produto = self._repository.get_produto(produto_id)
        if not produto:
            raise ValueError("produto inexistente")
        return produto


    @staticmethod
    def _ascii_key(value: Any) -> str:
        txt = unicodedata.normalize("NFD", str(value or ""))
        txt = "".join(ch for ch in txt if unicodedata.category(ch) != "Mn")
        txt = txt.lower()
        txt = re.sub(r"[^a-z0-9]+", "_", txt)
        return txt.strip("_")

    @classmethod
    def _safe_image_segment(cls, value: Any, fallback: str) -> str:
        segment = cls._ascii_key(value)
        if segment == "ao":
            segment = "aco"
        return segment or fallback

    def _build_uploaded_image_target(self, produto: Produto, extension: str) -> tuple[Path, str]:
        produto_id = int(produto.id or 0)
        empresa_key = self._safe_image_segment(produto.empresa_key, "empresa")
        produto_key_raw = str(produto.produto_key or "")
        ata_key_raw = str(produto.ata_key or "")
        if "__item_" in produto_key_raw and "__" in produto_key_raw:
            prefix = produto_key_raw.split("__item_", 1)[0]
            parts = prefix.split("__", 1)
            if len(parts) == 2 and parts[1].strip():
                ata_key_raw = parts[1]
        ata_key_raw = ata_key_raw.replace("__", "_")
        ata_key = self._safe_image_segment(ata_key_raw, "ata")
        item_key = self._safe_image_segment(produto.item_ata, f"{produto_id}")
        filename = f"item_{item_key}{extension}"
        target_dir = self._upload_root / empresa_key / ata_key
        relative_path = f"{self._upload_public_prefix}/{empresa_key}/{ata_key}/{filename}"
        return target_dir / filename, relative_path

    def _remove_previous_product_images(self, produto: Produto, target_path: Path) -> None:
        old_path_raw = str(produto.imagem_path or "").strip().replace("\\", "/")
        if old_path_raw.startswith(f"{self._upload_public_prefix}/"):
            old_rel = old_path_raw[len(self._upload_public_prefix) + 1 :]
            old_path = (self._upload_root / old_rel).resolve()
            try:
                if old_path.is_file() and self._upload_root.resolve() in old_path.parents and old_path != target_path.resolve():
                    old_path.unlink()
            except OSError:
                pass
        try:
            stem = target_path.stem
            for candidate in target_path.parent.glob(f"{stem}.*"):
                if candidate.is_file() and candidate.resolve() != target_path.resolve():
                    candidate.unlink()
        except OSError:
            pass

    def save_uploaded_imagem(self, produto_id: int, filename: str, content: bytes) -> Produto:
        produto = self.get_produto(produto_id)
        extension = Path((filename or "").strip()).suffix.lower()
        if extension not in self.IMAGE_EXTENSIONS:
            raise ValueError("extensao de imagem invalida")
        if not content:
            raise ValueError("arquivo de imagem vazio")
        if len(content) > self.IMAGE_MAX_BYTES:
            raise ValueError("imagem acima do limite de 5MB")
        target_path, relative_path = self._build_uploaded_image_target(produto, extension)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        self._remove_previous_product_images(produto, target_path)
        target_path.write_bytes(content)
        updated = self._repository.patch_imagem(produto_id, relative_path)
        if not updated:
            raise ValueError("produto inexistente")
        return updated

    @staticmethod
    def _bom_text(value: Any) -> Optional[str]:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    def _normalize_bom_item(self, item: BomItemInput) -> Dict[str, Any]:
        grupo = str(item.grupo).strip().lower()
        if grupo not in {"tubos", "chapas", "insumos"}:
            raise ValueError("grupo da BOM invalido")

        material = self._bom_text(item.material) or self._bom_text(item.item_nome)
        if not material:
            raise ValueError("material da BOM ausente")

        dim1 = self._bom_text(item.dim1) or self._bom_text(item.observacao)
        tamanho = self._bom_text(item.tamanho)
        unidade = self._bom_text(item.unidade)
        if grupo in {"tubos", "chapas"}:
            unidade = None
        else:
            tamanho = None

        return {
            "id": item.id,
            "grupo": grupo,
            "cod": self._bom_text(item.cod),
            "material": material,
            "dim1": dim1,
            "dim2": self._bom_text(item.dim2),
            "espessura": self._bom_text(item.espessura),
            "revestimento": self._bom_text(item.revestimento),
            "tamanho": tamanho,
            "unidade": unidade,
            "quantidade": item.quantidade,
            "item_nome": material,
            "observacao": dim1,
            "ordem": item.ordem,
        }

    def list_bom(self, produto_id: int) -> List[Dict[str, Any]]:
        _ = self.get_produto(produto_id)
        return self._repository.list_bom(produto_id)

    def list_bom_historico(self, produto_id: int) -> List[Dict[str, Any]]:
        _ = self.get_produto(produto_id)
        return self._repository.list_bom_historico(produto_id)

    def get_bom_ultima_atualizacao(self, produto_id: int) -> Optional[str]:
        _ = self.get_produto(produto_id)
        return self._repository.get_bom_ultima_atualizacao(produto_id)

    def clear_bom_historico(self, produto_id: int, created_by: Optional[str] = None) -> Dict[str, Any]:
        _ = self.get_produto(produto_id)
        return self._repository.clear_bom_history(produto_id, created_by=created_by or "painel_admin")

    @staticmethod
    def _bom_history_snapshot(item: Dict[str, Any]) -> Dict[str, Any]:
        keys = ("id", "grupo", "cod", "material", "dim1", "dim2", "espessura", "revestimento", "tamanho", "unidade", "quantidade")
        return {key: item.get(key) for key in keys if item.get(key) not in (None, "")}

    @staticmethod
    def _bom_compare_key(item: Dict[str, Any]) -> str:
        parts = [item.get(k) for k in ("grupo", "cod", "material", "dim1", "dim2", "espessura", "revestimento", "tamanho", "unidade")]
        return "|".join(str(p or "").strip().lower() for p in parts)

    @staticmethod
    def _bom_event_base(item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "grupo": item.get("grupo"),
            "cod": item.get("cod"),
            "material": item.get("material") or item.get("item_nome"),
            "bom_item_id": item.get("id"),
        }

    @staticmethod
    def _format_bom_field_name(field: str) -> str:
        labels = {"grupo": "Grupo", "cod": "COD", "material": "Material", "dim1": "DIM1", "dim2": "DIM2", "espessura": "Espessura", "revestimento": "Revestimento", "tamanho": "Tamanho", "unidade": "Unidade", "quantidade": "Quantidade"}
        return labels.get(field, field)

    def _build_bom_history_events(self, old_items: List[Dict[str, Any]], new_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        fields = ("grupo", "cod", "material", "dim1", "dim2", "espessura", "revestimento", "tamanho", "unidade", "quantidade")
        old_by_id = {int(item["id"]): item for item in old_items if item.get("id") is not None}
        used_old_ids: set[int] = set()
        for item in new_items:
            old: Optional[Dict[str, Any]] = None
            item_id = item.get("id")
            if item_id is not None:
                try:
                    old = old_by_id.get(int(item_id))
                except (TypeError, ValueError):
                    old = None
            if old is None:
                key = self._bom_compare_key(item)
                for candidate in old_items:
                    cid = candidate.get("id")
                    if cid in used_old_ids:
                        continue
                    if self._bom_compare_key(candidate) == key:
                        old = candidate
                        break
            if old is None:
                events.append({**self._bom_event_base(item), "acao": "ADICIONADO", "dados_antes": None, "dados_depois": self._bom_history_snapshot(item), "detalhe": "Item incluído na BOM"})
                continue
            if old.get("id") is not None:
                used_old_ids.add(int(old["id"]))
            changes: List[str] = []
            for field in fields:
                before = old.get(field)
                after = item.get(field)
                before_norm = "" if before is None else str(before).strip()
                after_norm = "" if after is None else str(after).strip()
                if before_norm != after_norm:
                    changes.append(f"{self._format_bom_field_name(field)}: {before_norm or '-'} -> {after_norm or '-'}")
            if changes:
                base = self._bom_event_base(item)
                base["bom_item_id"] = old.get("id") or base.get("bom_item_id")
                events.append({**base, "acao": "MODIFICADO", "dados_antes": self._bom_history_snapshot(old), "dados_depois": self._bom_history_snapshot(item), "detalhe": "; ".join(changes)})
        for old in old_items:
            oid = old.get("id")
            if oid is not None and int(oid) in used_old_ids:
                continue
            key = self._bom_compare_key(old)
            if any(self._bom_compare_key(item) == key for item in new_items):
                continue
            events.append({**self._bom_event_base(old), "acao": "REMOVIDO", "dados_antes": self._bom_history_snapshot(old), "dados_depois": None, "detalhe": "Item removido da BOM"})
        if events:
            events.append({"acao": "BOM_ATUALIZADA", "grupo": None, "cod": None, "material": None, "bom_item_id": None, "dados_antes": None, "dados_depois": {"eventos": len(events)}, "detalhe": f"BOM atualizada com {len(events)} alteração(ões)."})
        return events

    def add_bom_item(self, produto_id: int, item: BomItemInput) -> Dict[str, Any]:
        _ = self.get_produto(produto_id)
        payload = self._normalize_bom_item(item)
        row = self._repository.add_bom_item(
            produto_id=produto_id,
            grupo=payload["grupo"],
            cod=payload["cod"],
            material=payload["material"],
            dim1=payload["dim1"],
            dim2=payload["dim2"],
            espessura=payload["espessura"],
            revestimento=payload["revestimento"],
            tamanho=payload["tamanho"],
            quantidade=payload["quantidade"],
            unidade=payload["unidade"],
            item_nome=payload["item_nome"],
            observacao=payload["observacao"],
            ordem_item=payload["ordem"],
        )
        self._repository.add_bom_history_event(
            produto_id=produto_id,
            acao="ADICIONADO",
            grupo=row.get("grupo"),
            cod=row.get("cod"),
            material=row.get("material") or row.get("item_nome"),
            bom_item_id=row.get("id"),
            dados_depois=self._bom_history_snapshot(row),
            detalhe="Item incluído na BOM",
        )
        return row

    def replace_bom(self, produto_id: int, itens: List[BomItemInput]) -> List[Dict[str, Any]]:
        _ = self.get_produto(produto_id)
        old_items = self._repository.list_bom(produto_id)
        payload = [self._normalize_bom_item(i) for i in itens]
        events = self._build_bom_history_events(old_items, payload)
        rows = self._repository.replace_bom(produto_id, payload)
        if events:
            self._repository.add_bom_history_events(produto_id, events)
        return rows

    def delete_bom_item(self, produto_id: int, bom_item_id: int) -> bool:
        _ = self.get_produto(produto_id)
        old_item = next((item for item in self._repository.list_bom(produto_id) if int(item.get("id") or 0) == bom_item_id), None)
        ok = self._repository.delete_bom_item(produto_id, bom_item_id)
        if ok and old_item:
            self._repository.add_bom_history_event(
                produto_id=produto_id,
                acao="REMOVIDO",
                grupo=old_item.get("grupo"),
                cod=old_item.get("cod"),
                material=old_item.get("material") or old_item.get("item_nome"),
                bom_item_id=old_item.get("id"),
                dados_antes=self._bom_history_snapshot(old_item),
                detalhe="Item removido da BOM",
            )
        return ok

    def _imagem_existe(self, imagem_path: str) -> bool:
        rel_path = normalize_rel_path(imagem_path)
        return (self._image_root / rel_path).exists()

    def validate(self) -> ProdutosValidationReport:
        report = ProdutosValidationReport()
        produtos = self.list_produtos()
        report.total_produtos = len(produtos)

        seen_keys: Dict[str, int] = {}
        seen_item_scope: Dict[Tuple[str, str, str], int] = {}

        for index, produto in enumerate(produtos):
            row_ref = f"index={index}"
            if not produto.produto_key:
                report.erros.append(f"{row_ref}: produto_key ausente.")
            if not produto.nome_oficial:
                report.erros.append(f"{row_ref}: nome_oficial ausente.")

            if produto.empresa_key:
                report.empresas.add(produto.empresa_key)
            else:
                report.alertas.append(f"{row_ref}: empresa_key ausente.")

            if produto.ata_key:
                report.atas.add(produto.ata_key)
            else:
                report.alertas.append(f"{row_ref}: ata_key ausente.")

            if produto.categoria_key:
                report.categorias.add(produto.categoria_key)
            else:
                report.alertas.append(f"{row_ref}: categoria_key ausente.")

            if produto.imagem_path:
                if not self._imagem_existe(produto.imagem_path):
                    report.imagens_inexistentes.append(produto.imagem_path)
            else:
                report.produtos_sem_imagem.append(produto.produto_key or row_ref)

            if produto.produto_key:
                seen_keys[produto.produto_key] = seen_keys.get(produto.produto_key, 0) + 1

            if produto.item_ata and produto.empresa_key and produto.ata_key:
                scope = (produto.empresa_key, produto.ata_key, produto.item_ata)
                seen_item_scope[scope] = seen_item_scope.get(scope, 0) + 1

            if "arp_key" in produto.raw and "ata_key" in produto.raw:
                report.alertas.append(
                    f"{row_ref}: seed contem arp_key e ata_key; adapter usa ata_key e tolera arp_key."
                )

        report.duplicidades_produto_key = sorted([k for k, c in seen_keys.items() if c > 1])
        report.duplicidades_item_empresa_ata = sorted(
            [f"{e}|{a}|{i}" for (e, a, i), c in seen_item_scope.items() if c > 1]
        )

        if report.duplicidades_produto_key:
            report.erros.append("Duplicidade de produto_key encontrada.")
        if report.duplicidades_item_empresa_ata:
            report.alertas.append("Duplicidade de item_ata por empresa/ata encontrada.")
        return report
