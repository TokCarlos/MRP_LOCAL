from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.normalize import (
    EMPRESA_NOME_BY_KEY,
    ascii_key,
    build_produto_key,
    normalize_ata_key,
    normalize_ata_nome,
    normalize_empresa_key,
)
from app.core.paths import normalize_rel_path
from app.domain.produtos_models import BomItemInput
from app.repositories.produtos_repository import ProdutosRepository


class ProdutosService:
    IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
    IMAGE_MAX_BYTES = 5 * 1024 * 1024

    def __init__(
        self,
        repository: ProdutosRepository,
        image_root: Path,
        seed_path: Path,
        upload_root: Optional[Path] = None,
        upload_public_prefix: str = "media/produtos",
    ) -> None:
        self._repository = repository
        self._image_root = image_root
        self._seed_path = seed_path
        self._upload_root = upload_root or (image_root / "data" / "media" / "produtos")
        self._upload_public_prefix = upload_public_prefix.strip("/\\")

    def bootstrap_seed_if_needed(self) -> None:
        if self._repository.list_produtos():
            return
        if not self._seed_path.exists():
            return
        raw = json.loads(self._seed_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return
        for row in raw:
            if not isinstance(row, dict):
                continue
            empresa_raw = str(row.get("empresa_key") or row.get("empresa") or "").strip()
            if not empresa_raw:
                continue
            try:
                empresa_key = normalize_empresa_key(empresa_raw)
            except ValueError:
                continue
            if empresa_key == "tcr":
                continue
            ata_nome = normalize_ata_nome(str(row.get("arp") or row.get("ata_nome") or "").strip())
            numero_ata = str(row.get("ata_numero") or "").strip()
            item_ata = str(row.get("item_ata") or "").strip()
            nome_oficial = str(row.get("nome_oficial") or "").strip()
            if not ata_nome or not numero_ata or not item_ata or not nome_oficial:
                continue
            base = self.ensure_base(ata_nome=ata_nome, numero_ata=numero_ata, empresa_key=empresa_key)
            imagem_path = None
            imagem = row.get("imagem")
            if isinstance(imagem, dict):
                imagem_path = str(imagem.get("preview") or "").strip() or None
            if not imagem_path:
                imagem_path = str(row.get("imagem_path") or "").strip() or None
            categoria = str(row.get("categoria") or "").strip() or None
            produto_key = ascii_key(str(row.get("produto_key") or "").strip())
            if not produto_key:
                produto_key = build_produto_key(empresa_key, base["ata_key"], item_ata)
            try:
                self._repository.create_produto(
                    base_ata_id=int(base["id"]),
                    produto_key=produto_key,
                    item_ata=item_ata,
                    nome_oficial=nome_oficial,
                    categoria=categoria,
                    imagem_path=imagem_path,
                )
            except Exception:
                continue

    def _validate_empresa(self, empresa_key: str) -> str:
        try:
            normalized = normalize_empresa_key(empresa_key)
        except ValueError as exc:
            raise ValueError("empresa invalida") from exc
        return normalized

    def _validate_image_path(self, imagem_path: Optional[str]) -> Optional[str]:
        if not imagem_path:
            return None
        raw = imagem_path.strip()
        lower = raw.lower()
        if (
            lower.startswith("c:\\")
            or lower.startswith("x:\\")
            or lower.startswith("\\\\home-machine")
            or lower.startswith("http://")
            or lower.startswith("https://")
        ):
            raise ValueError("imagem invalida")
        if "pcp servidor\\pcp" in lower:
            raise ValueError("imagem invalida")
        return raw

    def list_produtos(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        return self._repository.list_produtos(include_inactive=include_inactive)

    def list_bases(self) -> List[Dict[str, Any]]:
        return self._repository.list_bases()

    def get_base(self, base_id: int) -> Optional[Dict[str, Any]]:
        return self._repository.get_base(base_id)

    def ensure_base(self, ata_nome: str, numero_ata: str, empresa_key: str) -> Dict[str, Any]:
        if not ata_nome.strip():
            raise ValueError("ata ausente")
        if not numero_ata.strip():
            raise ValueError("numero da ata ausente")
        empresa = self._validate_empresa(empresa_key)
        ata_nome_n = normalize_ata_nome(ata_nome)
        ata_key = normalize_ata_key(ata_nome_n, numero_ata)
        for base in self._repository.list_bases():
            if (
                base["ata_key"] == ata_key
                and base["numero_ata"] == numero_ata
                and base["empresa_key"] == empresa
            ):
                return base
        return self._repository.create_base(ata_nome_n, ata_key, numero_ata, empresa)

    def create_base(self, ata_nome: str, numero_ata: str, empresa_key: str) -> Dict[str, Any]:
        return self.ensure_base(ata_nome=ata_nome, numero_ata=numero_ata, empresa_key=empresa_key)

    def update_base(
        self, base_id: int, ata_nome: str, numero_ata: str, empresa_key: str, ativo: bool
    ) -> Dict[str, Any]:
        empresa = self._validate_empresa(empresa_key)
        ata_nome_n = normalize_ata_nome(ata_nome)
        ata_key = normalize_ata_key(ata_nome_n, numero_ata)
        updated = self._repository.update_base(base_id, ata_nome_n, ata_key, numero_ata, empresa, ativo)
        if not updated:
            raise ValueError("base inexistente")
        return updated

    def get_produto(self, produto_id: int) -> Dict[str, Any]:
        row = self._repository.get_produto(produto_id)
        if not row:
            raise ValueError("produto inexistente")
        return row

    def create_produto(
        self,
        base_ata_id: int,
        item_ata: str,
        nome_oficial: str,
        categoria: Optional[str],
        imagem_path: Optional[str],
    ) -> Dict[str, Any]:
        if not item_ata.strip():
            raise ValueError("item da ata ausente")
        if not nome_oficial.strip():
            raise ValueError("nome oficial ausente")
        base = self._repository.get_base(base_ata_id)
        if not base:
            raise ValueError("base inexistente")
        if base["empresa_key"] == "tcr":
            raise ValueError("tcr sem produtos nesta etapa")
        imagem = self._validate_image_path(imagem_path)
        produto_key = build_produto_key(base["empresa_key"], base["ata_key"], item_ata)
        for prod in self._repository.list_produtos():
            if prod.produto_key == produto_key:
                raise ValueError("produto duplicado")
        created = self._repository.create_produto(
            base_ata_id=base_ata_id,
            produto_key=produto_key,
            item_ata=item_ata.strip(),
            nome_oficial=nome_oficial.strip(),
            categoria=(categoria or "").strip() or None,
            imagem_path=imagem,
        )
        return created

    def update_produto(
        self,
        produto_id: int,
        base_ata_id: int,
        item_ata: str,
        nome_oficial: str,
        categoria: Optional[str],
        imagem_path: Optional[str],
        ativo: bool,
    ) -> Dict[str, Any]:
        _ = self.get_produto(produto_id)
        base = self._repository.get_base(base_ata_id)
        if not base:
            raise ValueError("base inexistente")
        if base["empresa_key"] == "tcr":
            raise ValueError("tcr sem produtos nesta etapa")
        if not item_ata.strip():
            raise ValueError("item da ata ausente")
        if not nome_oficial.strip():
            raise ValueError("nome oficial ausente")
        imagem = self._validate_image_path(imagem_path)
        updated = self._repository.update_produto(
            produto_id=produto_id,
            base_ata_id=base_ata_id,
            item_ata=item_ata.strip(),
            nome_oficial=nome_oficial.strip(),
            categoria=(categoria or "").strip() or None,
            imagem_path=imagem,
            ativo=ativo,
        )
        if not updated:
            raise ValueError("produto inexistente")
        return updated

    def patch_imagem(self, produto_id: int, imagem_path: Optional[str]) -> Dict[str, Any]:
        _ = self.get_produto(produto_id)
        imagem = self._validate_image_path(imagem_path)
        updated = self._repository.patch_imagem(produto_id, imagem)
        if not updated:
            raise ValueError("produto inexistente")
        return updated

    @staticmethod
    def _safe_image_segment(value: Any, fallback: str) -> str:
        segment = ascii_key(str(value or ""))
        return segment or fallback

    def _build_uploaded_image_target(self, produto: Dict[str, Any], extension: str) -> tuple[Path, str]:
        produto_id = int(produto.get("id") or 0)
        empresa_key = self._safe_image_segment(produto.get("empresa_key"), "empresa")
        produto_key_raw = str(produto.get("produto_key") or "")
        ata_key_raw = str(produto.get("ata_key") or "")
        if "__item_" in produto_key_raw and "__" in produto_key_raw:
            prefix = produto_key_raw.split("__item_", 1)[0]
            parts = prefix.split("__", 1)
            if len(parts) == 2 and parts[1].strip():
                ata_key_raw = parts[1]
        ata_key_raw = ata_key_raw.replace("__", "_")
        ata_key = self._safe_image_segment(ata_key_raw, "ata")
        item_key = self._safe_image_segment(produto.get("item_ata"), f"{produto_id}")
        filename = f"item_{item_key}{extension}"
        target_dir = self._upload_root / empresa_key / ata_key
        relative_path = f"{self._upload_public_prefix}/{empresa_key}/{ata_key}/{filename}"
        return target_dir / filename, relative_path

    def _remove_previous_product_images(self, produto: Dict[str, Any], target_path: Path) -> None:
        old_path_raw = str(produto.get("imagem_path") or "").strip().replace("\\", "/")
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

    def save_uploaded_imagem(self, produto_id: int, filename: str, content: bytes) -> Dict[str, Any]:
        produto = self.get_produto(produto_id)
        original_name = (filename or "").strip()
        extension = Path(original_name).suffix.lower()
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

    def inativar_produto(self, produto_id: int) -> bool:
        _ = self.get_produto(produto_id)
        return self._repository.soft_delete_produto(produto_id)

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

        dim1 = self._bom_text(item.dim1)
        # Compatibilidade: antes observacao era usado como DIM1 na UI provisoria.
        if not dim1:
            dim1 = self._bom_text(item.observacao)

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

    @staticmethod
    def _bom_history_snapshot(item: Dict[str, Any]) -> Dict[str, Any]:
        keys = ("id", "grupo", "cod", "material", "dim1", "dim2", "espessura", "revestimento", "tamanho", "unidade", "quantidade")
        return {key: item.get(key) for key in keys if item.get(key) not in (None, "")}

    @staticmethod
    def _bom_compare_key(item: Dict[str, Any]) -> str:
        parts = [
            item.get("grupo"),
            item.get("cod"),
            item.get("material"),
            item.get("dim1"),
            item.get("dim2"),
            item.get("espessura"),
            item.get("revestimento"),
            item.get("tamanho"),
            item.get("unidade"),
        ]
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
        labels = {
            "grupo": "Grupo",
            "cod": "COD",
            "material": "Material",
            "dim1": "DIM1",
            "dim2": "DIM2",
            "espessura": "Espessura",
            "revestimento": "Revestimento",
            "tamanho": "Tamanho",
            "unidade": "Unidade",
            "quantidade": "Quantidade",
        }
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
                base = self._bom_event_base(item)
                events.append({
                    **base,
                    "acao": "ADICIONADO",
                    "dados_antes": None,
                    "dados_depois": self._bom_history_snapshot(item),
                    "detalhe": "Item incluído na BOM",
                })
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
                events.append({
                    **base,
                    "acao": "MODIFICADO",
                    "dados_antes": self._bom_history_snapshot(old),
                    "dados_depois": self._bom_history_snapshot(item),
                    "detalhe": "; ".join(changes),
                })

        for old in old_items:
            oid = old.get("id")
            if oid is not None and int(oid) in used_old_ids:
                continue
            key = self._bom_compare_key(old)
            if any(self._bom_compare_key(item) == key for item in new_items):
                continue
            base = self._bom_event_base(old)
            events.append({
                **base,
                "acao": "REMOVIDO",
                "dados_antes": self._bom_history_snapshot(old),
                "dados_depois": None,
                "detalhe": "Item removido da BOM",
            })

        if events:
            events.append({
                "acao": "BOM_ATUALIZADA",
                "grupo": None,
                "cod": None,
                "material": None,
                "bom_item_id": None,
                "dados_antes": None,
                "dados_depois": {"eventos": len(events)},
                "detalhe": f"BOM atualizada com {len(events)} alteração(ões).",
            })
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

    def imagem_existe(self, imagem_path: str) -> bool:
        rel_path = normalize_rel_path(imagem_path)
        if rel_path.startswith("media/"):
            return (self._upload_root.parent / rel_path.removeprefix("media/")).exists()
        return (self._image_root / rel_path).exists()

    def make_contract_item(self, row: Dict[str, Any]) -> Dict[str, Any]:
        imagem = row.get("imagem_path")
        return {
            "id": row.get("id"),
            "produto_key": row.get("produto_key"),
            "item_ata": row.get("item_ata"),
            "nome_oficial": row.get("nome_oficial"),
            "categoria": row.get("categoria"),
            "imagem_path": imagem,
            "imagem_url": imagem,
            "imagem": {"preview": imagem} if imagem else {"preview": None},
            "ativo": bool(row.get("ativo", 1)),
            "base_ata_id": row.get("base_ata_id"),
            "ata_key": row.get("ata_key"),
            "ata_numero": row.get("numero_ata"),
            "arp": row.get("ata_nome"),
            "empresa_key": row.get("empresa_key"),
            "empresa": row.get("empresa_nome"),
            "created_at": row.get("created_at"),
            "updated_at": row.get("updated_at"),
        }
