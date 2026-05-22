from __future__ import annotations

from app.config import AppConfig
from app.contracts.health_contract import build_health_contract


def get_health(cfg: AppConfig) -> dict[str, object]:
    return build_health_contract(cfg.version)

