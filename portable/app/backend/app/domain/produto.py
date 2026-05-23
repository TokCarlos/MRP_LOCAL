from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Produto:
    id: Optional[int]
    produto_key: str
    empresa_key: Optional[str]
    ata_key: Optional[str]
    categoria_key: Optional[str]
    item_ata: Optional[str]
    nome_oficial: str
    nome_busca: str
    imagem_path: Optional[str]
    ativo: bool
    raw: Dict[str, Any]

    @staticmethod
    def _first_text(raw: Dict[str, Any], keys: list[str]) -> Optional[str]:
        for key in keys:
            value = raw.get(key)
            if value is None:
                continue
            text = str(value).strip()
            if text:
                return text
        return None

    @classmethod
    def from_seed(cls, raw: Dict[str, Any]) -> "Produto":
        imagem = raw.get("imagem")
        imagem_path = None
        if isinstance(imagem, dict):
            imagem_path = cls._first_text(imagem, ["preview", "path", "arquivo"])
        if not imagem_path:
            imagem_path = cls._first_text(raw, ["imagem_path", "imagem_preview", "imagem"])

        nome_oficial = cls._first_text(raw, ["nome_oficial", "nome", "produto_nome"]) or ""
        status = cls._first_text(raw, ["status", "ativo"]) or "ATIVO"
        ativo = status.upper() in {"ATIVO", "TRUE", "1", "SIM"}

        return cls(
            id=raw.get("id") if isinstance(raw.get("id"), int) else None,
            produto_key=cls._first_text(raw, ["produto_key", "key", "id_key"]) or "",
            empresa_key=cls._first_text(raw, ["empresa_key", "empresa"]),
            ata_key=cls._first_text(raw, ["ata_key", "arp_key", "ata_numero"]),
            categoria_key=cls._first_text(raw, ["categoria_key", "categoria"]),
            item_ata=cls._first_text(raw, ["item_ata", "item", "item_key"]),
            nome_oficial=nome_oficial,
            nome_busca=nome_oficial.casefold(),
            imagem_path=imagem_path,
            ativo=ativo,
            raw=raw,
        )

    def to_contract(self) -> Dict[str, Any]:
        empresa_nome = self.raw.get("empresa_nome") or self.raw.get("empresa") or self.empresa_key
        if str(self.empresa_key or empresa_nome or "").strip().lower() in {"aco", "ao", "aço"}:
            empresa_nome = "Aço"
        return {
            "id": self.id,
            "produto_key": self.produto_key,
            "empresa_key": "aco" if str(self.empresa_key or "").strip().lower() in {"aco", "ao", "aço"} else self.empresa_key,
            "empresa_nome": empresa_nome,
            "empresa": empresa_nome,
            "ata_key": self.ata_key,
            "categoria_key": self.categoria_key,
            "item_ata": self.item_ata,
            "nome_oficial": self.nome_oficial,
            "nome_busca": self.nome_busca,
            "imagem_path": self.imagem_path,
            "imagem_url": self.imagem_path,
            "imagem": {"preview": self.imagem_path} if self.imagem_path else {"preview": None},
            "ativo": self.ativo,
        }
