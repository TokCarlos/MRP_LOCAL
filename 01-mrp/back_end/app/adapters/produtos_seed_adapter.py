from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class ProdutosSeedAdapter:
    def __init__(self, project_root: Path | None = None) -> None:
        self._project_root = project_root or Path(__file__).resolve().parents[4]

    @property
    def project_root(self) -> Path:
        return self._project_root

    @property
    def seed_path(self) -> Path:
        return self.project_root / "01-mrp" / "front_end" / "data" / "produtos_seed.json"

    def load_raw_data(self) -> Any:
        content = self.seed_path.read_text(encoding="utf-8")
        data = json.loads(content)
        if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
            data = data[0]
        return data

    def load_produtos(self) -> List[Dict[str, Any]]:
        data = self.load_raw_data()
        if not isinstance(data, list):
            raise ValueError("produtos_seed.json precisa ser uma lista de produtos.")
        normalized: List[Dict[str, Any]] = []
        for idx, row in enumerate(data):
            if not isinstance(row, dict):
                raise ValueError(f"Registro na posicao {idx} nao e objeto JSON.")
            normalized.append(row)
        return normalized
