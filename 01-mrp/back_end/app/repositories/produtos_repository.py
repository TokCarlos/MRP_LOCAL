from __future__ import annotations

from typing import List

from adapters.produtos_seed_adapter import ProdutosSeedAdapter
from domain.produto import Produto


class ProdutosRepository:
    def __init__(self, adapter: ProdutosSeedAdapter) -> None:
        self._adapter = adapter

    def list_produtos(self) -> List[Produto]:
        rows = self._adapter.load_produtos()
        return [Produto.from_seed(row) for row in rows]
