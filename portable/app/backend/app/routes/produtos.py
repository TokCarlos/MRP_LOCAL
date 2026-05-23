from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.adapters.produtos_seed_adapter import ProdutosSeedAdapter
from app.config import AppConfig
from app.contracts.error_contract import build_error_contract
from app.contracts.produtos_contract import build_produtos_contract
from app.core.errors import BackendError
from app.domain.produtos_models import BomItemInput, BomReplaceInput
from app.repositories.produtos_repository import ProdutosRepository
from app.services.produtos_service import ProdutosService


def _err(code: str, message: str, status: int = 400) -> HTTPException:
    return HTTPException(status_code=status, detail={"ok": False, "error": {"code": code, "message": message}})


def build_router(cfg: AppConfig) -> APIRouter:
    router = APIRouter(prefix="/api")
    adapter = ProdutosSeedAdapter(seed_path=cfg.produtos_seed_path)
    repository = ProdutosRepository(
        adapter=adapter,
        bom_path=cfg.produtos_bom_path,
        bom_historico_path=cfg.produtos_bom_historico_path,
        imagem_state_path=cfg.produtos_imagem_state_path,
    )
    service = ProdutosService(
        repository=repository,
        image_root=cfg.produtos_image_root,
        upload_root=cfg.produtos_upload_root,
        upload_public_prefix=cfg.produtos_upload_public_prefix,
    )

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


    @router.post("/produtos/{produto_id:int}/imagem/upload")
    async def upload_imagem(produto_id: int, arquivo: UploadFile = File(...)) -> dict[str, object]:
        try:
            content = await arquivo.read()
            row = service.save_uploaded_imagem(produto_id, arquivo.filename or "", content)
            return {"ok": True, "data": row.to_contract()}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.get("/produtos/{produto_id:int}/bom")
    def get_bom(produto_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_bom(produto_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.get("/produtos/{produto_id:int}/bom/ultima-atualizacao")
    def get_bom_ultima_atualizacao(produto_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": {"ultima_atualizacao_bom": service.get_bom_ultima_atualizacao(produto_id)}}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.get("/produtos/{produto_id:int}/bom/historico")
    def get_bom_historico(produto_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_bom_historico(produto_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.delete("/produtos/{produto_id:int}/bom/historico")
    def clear_bom_historico(produto_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.clear_bom_historico(produto_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.post("/produtos/{produto_id:int}/bom")
    def add_bom_item(produto_id: int, payload: BomItemInput) -> dict[str, object]:
        try:
            row = service.add_bom_item(produto_id, payload)
            return {"ok": True, "data": row}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.put("/produtos/{produto_id:int}/bom")
    def replace_bom(produto_id: int, payload: BomReplaceInput) -> dict[str, object]:
        try:
            rows = service.replace_bom(produto_id, payload.itens)
            return {"ok": True, "data": rows}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.delete("/produtos/{produto_id:int}/bom/{bom_item_id:int}")
    def delete_bom_item(produto_id: int, bom_item_id: int) -> dict[str, object]:
        try:
            ok = service.delete_bom_item(produto_id, bom_item_id)
            return {"ok": True, "data": {"inativado": ok}}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    return router
