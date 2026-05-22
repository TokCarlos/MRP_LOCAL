from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import AppConfig
from app.domain.produtos_models import (
    BaseAtaCreate,
    BaseAtaUpdate,
    BomItemInput,
    BomReplaceInput,
    ProdutoCreate,
    ProdutoImagemPatch,
    ProdutoUpdate,
)
from app.repositories.produtos_repository import ProdutosRepository
from app.services.produtos_service import ProdutosService


def _err(code: str, message: str, status: int = 400) -> HTTPException:
    return HTTPException(status_code=status, detail={"ok": False, "error": {"code": code, "message": message}})


def build_router(cfg: AppConfig) -> APIRouter:
    router = APIRouter(prefix="/api")
    repository = ProdutosRepository(db_path=cfg.db_path, migration_path=cfg.db_migration_path)
    service = ProdutosService(
        repository=repository,
        image_root=cfg.produtos_image_root,
        seed_path=cfg.produtos_seed_path,
        upload_root=cfg.produtos_upload_root,
        upload_public_prefix=cfg.produtos_upload_public_prefix,
    )
    service.bootstrap_seed_if_needed()

    @router.get("/produtos")
    def produtos() -> dict[str, object]:
        try:
            rows = [service.make_contract_item(p.raw) for p in service.list_produtos()]
            return {"ok": True, "data": rows}
        except ValueError as exc:
            raise _err("validation_error", str(exc), 400) from exc
        except Exception as exc:
            raise _err("service_unavailable", f"Servico indisponivel: {exc}", 500) from exc

    @router.get("/produtos/{produto_id:int}")
    def get_produto(produto_id: int) -> dict[str, object]:
        try:
            row = service.get_produto(produto_id)
            return {"ok": True, "data": service.make_contract_item(row)}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.post("/produtos")
    def create_produto(payload: ProdutoCreate) -> dict[str, object]:
        try:
            row = service.create_produto(
                base_ata_id=payload.base_ata_id,
                item_ata=payload.item_ata,
                nome_oficial=payload.nome_oficial,
                categoria=payload.categoria,
                imagem_path=payload.imagem_path,
            )
            return {"ok": True, "data": service.make_contract_item(row)}
        except ValueError as exc:
            msg = str(exc)
            status = 409 if "duplicado" in msg else 400
            raise _err("validation_error", msg, status) from exc

    @router.put("/produtos/{produto_id:int}")
    def update_produto(produto_id: int, payload: ProdutoUpdate) -> dict[str, object]:
        try:
            row = service.update_produto(
                produto_id=produto_id,
                base_ata_id=payload.base_ata_id,
                item_ata=payload.item_ata,
                nome_oficial=payload.nome_oficial,
                categoria=payload.categoria,
                imagem_path=payload.imagem_path,
                ativo=payload.ativo,
            )
            return {"ok": True, "data": service.make_contract_item(row)}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.patch("/produtos/{produto_id:int}/imagem")
    def patch_imagem(produto_id: int, payload: ProdutoImagemPatch) -> dict[str, object]:
        try:
            row = service.patch_imagem(produto_id, payload.imagem_path)
            return {"ok": True, "data": service.make_contract_item(row)}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.post("/produtos/{produto_id:int}/imagem/upload")
    async def upload_imagem(produto_id: int, arquivo: UploadFile = File(...)) -> dict[str, object]:
        try:
            content = await arquivo.read()
            row = service.save_uploaded_imagem(produto_id, arquivo.filename or "", content)
            return {"ok": True, "data": service.make_contract_item(row)}
        except ValueError as exc:
            msg = str(exc)
            code = "not_found" if "inexistente" in msg else "validation_error"
            status = 404 if code == "not_found" else 400
            raise _err(code, msg, status) from exc

    @router.delete("/produtos/{produto_id:int}")
    def delete_produto(produto_id: int) -> dict[str, object]:
        try:
            ok = service.inativar_produto(produto_id)
            return {"ok": True, "data": {"inativado": ok}}
        except ValueError as exc:
            raise _err("not_found", str(exc), 404) from exc

    @router.get("/produtos/bases")
    def list_bases() -> dict[str, object]:
        return {"ok": True, "data": service.list_bases()}

    @router.post("/produtos/bases")
    def create_base(payload: BaseAtaCreate) -> dict[str, object]:
        try:
            base = service.create_base(payload.ata_nome, payload.numero_ata, payload.empresa_key)
            return {"ok": True, "data": base}
        except ValueError as exc:
            raise _err("validation_error", str(exc), 400) from exc

    @router.get("/produtos/bases/{base_id:int}")
    def get_base(base_id: int) -> dict[str, object]:
        base = service.get_base(base_id)
        if not base:
            raise _err("not_found", "base inexistente", 404)
        return {"ok": True, "data": base}

    @router.put("/produtos/bases/{base_id:int}")
    def update_base(base_id: int, payload: BaseAtaUpdate) -> dict[str, object]:
        try:
            base = service.update_base(
                base_id=base_id,
                ata_nome=payload.ata_nome,
                numero_ata=payload.numero_ata,
                empresa_key=payload.empresa_key,
                ativo=payload.ativo,
            )
            return {"ok": True, "data": base}
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
