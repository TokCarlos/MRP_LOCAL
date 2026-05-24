from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.adapters.produtos_seed_adapter import ProdutosSeedAdapter
from app.config import AppConfig
from app.domain.ordens_producao_models import (
    OrdemBomUpdate,
    OrdemProcessoUpdate,
    OrdemProducaoCreate,
    OrdemProducaoUpdate,
    OrdemProdutoCreate,
    OrdemProdutoUpdate,
)
from app.repositories.ordens_producao_repository import OrdensProducaoRepository
from app.repositories.produtos_repository import ProdutosRepository
from app.services.ordens_producao_service import OrdensProducaoService


def _err(code: str, message: str, status: int = 400) -> HTTPException:
    return HTTPException(status_code=status, detail={"ok": False, "error": {"code": code, "message": message}})


def build_router(cfg: AppConfig) -> APIRouter:
    router = APIRouter(prefix="/api")
    ordens_repository = OrdensProducaoRepository(runtime_path=cfg.project_root / "runtime" / "ordens_producao.json")
    produtos_repository = ProdutosRepository(
        adapter=ProdutosSeedAdapter(seed_path=cfg.produtos_seed_path),
        bom_path=cfg.produtos_bom_path,
        bom_historico_path=cfg.produtos_bom_historico_path,
        imagem_state_path=cfg.produtos_imagem_state_path,
    )
    service = OrdensProducaoService(repository=ordens_repository, produtos_repository=produtos_repository)

    @router.get("/ordens-producao")
    def list_ordens() -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_ordens()}
        except Exception as exc:
            raise _err("service_unavailable", f"Servico indisponivel: {exc}", 500) from exc

    @router.post("/ordens-producao")
    def create_ordem(payload: OrdemProducaoCreate) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.create_ordem(payload.model_dump(exclude_unset=True))}
        except ValueError as exc:
            raise _err("validation_error", str(exc), 400) from exc

    @router.get("/ordens-producao/{op_id:int}")
    def get_ordem(op_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.get_ordem(op_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.put("/ordens-producao/{op_id:int}")
    def update_ordem(op_id: int, payload: OrdemProducaoUpdate) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.update_ordem(op_id, payload.model_dump(exclude_unset=True))}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.delete("/ordens-producao/{op_id:int}")
    def delete_ordem(op_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.delete_ordem(op_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.get("/ordens-producao/{op_id:int}/produtos")
    def list_op_produtos(op_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_op_produtos(op_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.post("/ordens-producao/{op_id:int}/produtos")
    def add_op_produto(op_id: int, payload: OrdemProdutoCreate) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.add_op_produto(op_id, payload.model_dump(exclude_unset=True))}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.put("/ordens-producao/{op_id:int}/produtos/{op_produto_id:int}")
    def update_op_produto(op_id: int, op_produto_id: int, payload: OrdemProdutoUpdate) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.update_op_produto(op_id, op_produto_id, payload.model_dump(exclude_unset=True))}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.delete("/ordens-producao/{op_id:int}/produtos/{op_produto_id:int}")
    def delete_op_produto(op_id: int, op_produto_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.remove_op_produto(op_id, op_produto_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.get("/ordens-producao/{op_id:int}/bom")
    def list_bom(op_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_bom(op_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.put("/ordens-producao/{op_id:int}/bom")
    def update_bom(op_id: int, payload: OrdemBomUpdate) -> dict[str, object]:
        try:
            items = [item.model_dump(exclude_unset=True) for item in payload.itens]
            return {"ok": True, "data": service.update_bom(op_id, items)}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.get("/ordens-producao/{op_id:int}/processos")
    def list_processos(op_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_processos(op_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.put("/ordens-producao/{op_id:int}/processos/{processo_id:int}")
    def update_processo(op_id: int, processo_id: int, payload: OrdemProcessoUpdate) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.update_processo(op_id, processo_id, payload.model_dump(exclude_unset=True))}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.get("/ordens-producao/{op_id:int}/historico")
    def list_historico(op_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_historico(op_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    return router
