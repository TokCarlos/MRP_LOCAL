from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.adapters.produtos_seed_adapter import ProdutosSeedAdapter
from app.config import AppConfig
from app.contracts.error_contract import build_error_contract
from app.contracts.produtos_contract import build_produtos_contract
from app.core.errors import BackendError
from app.repositories.produtos_repository import ProdutosRepository
from app.services.produtos_service import ProdutosService


def build_router(cfg: AppConfig) -> APIRouter:
    router = APIRouter(prefix="/api")
    adapter = ProdutosSeedAdapter(seed_path=cfg.produtos_seed_path)
    repository = ProdutosRepository(adapter=adapter)
    service = ProdutosService(repository=repository, image_root=cfg.produtos_image_root)

    @router.get("/produtos")
    def produtos() -> dict[str, object]:
        try:
            produtos_data = service.list_produtos()
            return build_produtos_contract(produtos_data)
        except BackendError as exc:
            raise HTTPException(
                status_code=exc.status_code, detail=build_error_contract(exc.code, exc.message)
            ) from exc
        except Exception as exc:
            detail = build_error_contract("service_unavailable", f"Servico indisponivel: {exc}")
            raise HTTPException(status_code=500, detail=detail) from exc

    return router

