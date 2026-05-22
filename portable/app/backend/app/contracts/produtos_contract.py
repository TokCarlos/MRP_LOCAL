from __future__ import annotations

from typing import Any, Dict, List

from app.domain.produto import Produto


def build_produtos_contract(produtos: List[Produto]) -> Dict[str, Any]:
    items = [produto.to_contract() for produto in produtos]
    return {"ok": True, "source": "seed", "count": len(items), "items": items}

