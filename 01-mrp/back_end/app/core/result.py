from __future__ import annotations

from typing import Any, Dict


def ok_response(**payload: Any) -> Dict[str, Any]:
    response: Dict[str, Any] = {"ok": True}
    response.update(payload)
    return response


def error_response(code: str, message: str) -> Dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message}}

