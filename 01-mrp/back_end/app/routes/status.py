from __future__ import annotations

from fastapi import APIRouter

from app.config import AppConfig
from app.services.status_service import get_status


def build_router(cfg: AppConfig) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/status")
    def status() -> dict[str, object]:
        return get_status(cfg)

    return router

