from __future__ import annotations

from typing import Dict


def build_error_contract(code: str, message: str) -> Dict[str, object]:
    return {"ok": False, "error": {"code": code, "message": message}}

