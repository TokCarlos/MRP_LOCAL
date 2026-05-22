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
        upload_public_prefix: str = "assets/images/produtos",
    ) -> None:
        self._repository = repository
        self._image_root = image_root
        self._seed_path = seed_path
        self._upload_root = upload_root or (image_root / "assets" / "images" / "produtos")
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
            produto_key = str(row.get("produto_key") or "").strip()
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

    def list_produtos(self) -> List[Dict[str, Any]]:
        return self._repository.list_produtos()

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

        key = ascii_key(str(produto.get("produto_key") or f"produto_{produto_id}")) or f"produto_{produto_id}"
        target_name = f"{key}{extension}"
        self._upload_root.mkdir(parents=True, exist_ok=True)
        target_path = self._upload_root / target_name
        target_path.write_bytes(content)

        relative_path = f"{self._upload_public_prefix}/{target_name}"
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

    def add_bom_item(self, produto_id: int, item: BomItemInput) -> Dict[str, Any]:
        _ = self.get_produto(produto_id)
        return self._repository.add_bom_item(
            produto_id=produto_id,
            grupo=item.grupo,
            item_nome=item.item_nome.strip(),
            quantidade=item.quantidade,
            unidade=(item.unidade or "").strip() or None,
            observacao=(item.observacao or "").strip() or None,
            ordem_item=item.ordem,
        )

    def replace_bom(self, produto_id: int, itens: List[BomItemInput]) -> List[Dict[str, Any]]:
        _ = self.get_produto(produto_id)
        payload = [
            {
                "grupo": i.grupo,
                "item_nome": i.item_nome.strip(),
                "quantidade": i.quantidade,
                "unidade": (i.unidade or "").strip() or None,
                "observacao": (i.observacao or "").strip() or None,
                "ordem": i.ordem,
            }
            for i in itens
        ]
        return self._repository.replace_bom(produto_id, payload)

    def delete_bom_item(self, produto_id: int, bom_item_id: int) -> bool:
        _ = self.get_produto(produto_id)
        return self._repository.delete_bom_item(produto_id, bom_item_id)

    def imagem_existe(self, imagem_path: str) -> bool:
        rel_path = normalize_rel_path(imagem_path)
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
            "imagem": {"preview": imagem} if imagem else {"preview": None},
            "ativo": bool(row.get("ativo", 1)),
            "base_ata_id": row.get("base_ata_id"),
            "ata_key": row.get("ata_key"),
            "ata_numero": row.get("numero_ata"),
            "arp": row.get("ata_nome"),
            "empresa_key": row.get("empresa_key"),
            "empresa": row.get("empresa_nome"),
        }
