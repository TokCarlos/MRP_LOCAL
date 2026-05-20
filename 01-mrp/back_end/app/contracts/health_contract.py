from __future__ import annotations

from typing import Dict


def build_health_contract(version: str) -> Dict[str, object]:
    return {"ok": True, "service": "mrp_backend", "version": version}

