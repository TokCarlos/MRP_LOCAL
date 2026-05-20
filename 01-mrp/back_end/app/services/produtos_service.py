from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

from domain.produto import Produto
from repositories.produtos_repository import ProdutosRepository


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
    def __init__(self, repository: ProdutosRepository, project_root: Path) -> None:
        self._repository = repository
        self._project_root = project_root

    def _imagem_existe(self, imagem_path: str) -> bool:
        normalized_parts = [part for part in imagem_path.replace("\\", "/").split("/") if part]
        path = self._project_root / "01-mrp" / "front_end" / Path(*normalized_parts)
        return path.exists()

    def validate(self) -> ProdutosValidationReport:
        report = ProdutosValidationReport()
        produtos: List[Produto] = self._repository.list_produtos()
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
                report.alertas.append(f"{row_ref}: categoria ausente.")

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
