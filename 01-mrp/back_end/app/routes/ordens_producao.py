from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.config import AppConfig
from app.domain.ordens_producao_models import (
    OrdemBomUpdate,
    OrdemKanbanMoverProximo,
    OrdemKanbanPular,
    OrdemKanbanStatusUpdate,
    OrdemProcessoUpdate,
    OrdemProducaoCreate,
    OrdemProducaoUpdate,
    OrdemProdutoCreate,
    OrdemProdutoUpdate,
)
from app.repositories.ordens_producao_repository import OrdensProducaoRepository
from app.services.ordens_producao_service import OrdensProducaoService


def _err(code: str, message: str, status: int = 400) -> HTTPException:
    return HTTPException(status_code=status, detail={"ok": False, "error": {"code": code, "message": message}})


def build_router(cfg: AppConfig) -> APIRouter:
    router = APIRouter(prefix="/api")
    repository = OrdensProducaoRepository(db_path=cfg.db_path, migration_path=cfg.db_migration_path)
    service = OrdensProducaoService(repository=repository)

    @router.get("/ordens-producao")
    def list_ordens() -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_ordens()}
        except Exception as exc:
            raise _err("service_unavailable", f"Servico indisponivel: {exc}", 500) from exc

    @router.get("/ordens-producao/kanban")
    def list_ordens_kanban() -> dict[str, object]:
        try:
            return {"ok": True, "data": service.list_kanban()}
        except Exception as exc:
            raise _err("service_unavailable", f"Servico indisponivel: {exc}", 500) from exc

    @router.post("/ordens-producao")
    def create_ordem(payload: OrdemProducaoCreate) -> dict[str, object]:
        try:
            created = service.create_ordem(payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": created}
        except ValueError as exc:
            raise _err("validation_error", str(exc), 400) from exc

    @router.post("/ordens-producao/{op_id:int}/kanban/status")
    def set_kanban_status(op_id: int, payload: OrdemKanbanStatusUpdate) -> dict[str, object]:
        try:
            updated = service.set_kanban_status(op_id, payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": updated}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.post("/ordens-producao/{op_id:int}/kanban/mover-proximo")
    def move_kanban_next(op_id: int, payload: OrdemKanbanMoverProximo) -> dict[str, object]:
        try:
            updated = service.mover_kanban_proximo(op_id, payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": updated}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.post("/ordens-producao/{op_id:int}/kanban/pular")
    def jump_kanban_step(op_id: int, payload: OrdemKanbanPular) -> dict[str, object]:
        try:
            updated = service.pular_kanban_processo(op_id, payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": updated}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.get("/ordens-producao/{op_id:int}")
    def get_ordem(op_id: int) -> dict[str, object]:
        try:
            return {"ok": True, "data": service.get_ordem(op_id)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.put("/ordens-producao/{op_id:int}")
    def update_ordem(op_id: int, payload: OrdemProducaoUpdate) -> dict[str, object]:
        try:
            updated = service.update_ordem(op_id, payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": updated}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.delete("/ordens-producao/{op_id:int}")
    def delete_ordem(op_id: int) -> dict[str, object]:
        try:
            deleted = service.delete_ordem(op_id)
            return {"ok": True, "data": deleted}
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
            created = service.add_op_produto(op_id, payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": created}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.put("/ordens-producao/{op_id:int}/produtos/{op_produto_id:int}")
    def update_op_produto(op_id: int, op_produto_id: int, payload: OrdemProdutoUpdate) -> dict[str, object]:
        try:
            updated = service.update_op_produto(op_id, op_produto_id, payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": updated}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.delete("/ordens-producao/{op_id:int}/produtos/{op_produto_id:int}")
    def delete_op_produto(op_id: int, op_produto_id: int) -> dict[str, object]:
        try:
            deleted = service.remove_op_produto(op_id, op_produto_id)
            return {"ok": True, "data": deleted}
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
            updated = service.update_bom(op_id, items)
            return {"ok": True, "data": updated}
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
            updated = service.update_processo(op_id, processo_id, payload.model_dump(exclude_unset=True))
            return {"ok": True, "data": updated}
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
