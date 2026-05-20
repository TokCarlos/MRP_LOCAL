from __future__ import annotations

from app.config import AppConfig
from app.contracts.status_contract import build_status_contract


def get_status(cfg: AppConfig) -> dict[str, object]:
    return build_status_contract(cfg)

