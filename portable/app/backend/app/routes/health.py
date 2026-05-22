from __future__ import annotations

from fastapi import APIRouter

from app.config import AppConfig
from app.services.health_service import get_health


def build_router(cfg: AppConfig) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict[str, object]:
        return get_health(cfg)

    return router

