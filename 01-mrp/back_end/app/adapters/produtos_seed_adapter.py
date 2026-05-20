from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from app.core.encoding import read_utf8_text
from app.core.errors import AdapterError, SeedInvalidError, SeedNotFoundError


class ProdutosSeedAdapter:
    def __init__(self, seed_path: Path) -> None:
        self._seed_path = seed_path

    @property
    def seed_path(self) -> Path:
        return self._seed_path

    def load_raw_data(self) -> Any:
        if not self.seed_path.exists():
            raise SeedNotFoundError(str(self.seed_path))
        try:
            content = read_utf8_text(self.seed_path)
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise SeedInvalidError(f"JSON invalido no seed de produtos: {exc}") from exc
        except OSError as exc:
            raise AdapterError(f"Falha ao ler seed de produtos: {exc}") from exc

        if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
            data = data[0]
        return data

    def load_produtos(self) -> List[Dict[str, Any]]:
        data = self.load_raw_data()
        if not isinstance(data, list):
            raise SeedInvalidError("produtos_seed.json precisa ser uma lista de produtos.")
        normalized: List[Dict[str, Any]] = []
        for idx, row in enumerate(data):
            if not isinstance(row, dict):
                raise SeedInvalidError(f"Registro na posicao {idx} nao e objeto JSON.")
            normalized.append(row)
        return normalized
