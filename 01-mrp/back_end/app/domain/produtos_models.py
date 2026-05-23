from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


EmpresaKey = Literal["jpl", "aco", "tcr"]
BomGrupo = Literal["tubos", "chapas", "insumos"]


class BaseAtaCreate(BaseModel):
    ata_nome: str = Field(min_length=1)
    numero_ata: str = Field(min_length=1)
    empresa_key: EmpresaKey


class BaseAtaUpdate(BaseModel):
    ata_nome: str = Field(min_length=1)
    numero_ata: str = Field(min_length=1)
    empresa_key: EmpresaKey
    ativo: bool = True


class ProdutoCreate(BaseModel):
    base_ata_id: int
    item_ata: str = Field(min_length=1)
    nome_oficial: str = Field(min_length=1)
    categoria: Optional[str] = None
    imagem_path: Optional[str] = None


class ProdutoUpdate(BaseModel):
    base_ata_id: int
    item_ata: str = Field(min_length=1)
    nome_oficial: str = Field(min_length=1)
    categoria: Optional[str] = None
    imagem_path: Optional[str] = None
    ativo: bool = True


class ProdutoImagemPatch(BaseModel):
    imagem_path: Optional[str] = None


class BomItemInput(BaseModel):
    id: Optional[int] = None
    grupo: BomGrupo

    # Novo contrato estruturado da BOM.
    cod: Optional[str] = None
    material: Optional[str] = None
    dim1: Optional[str] = None
    dim2: Optional[str] = None
    espessura: Optional[str] = None
    revestimento: Optional[str] = None
    tamanho: Optional[str] = None
    unidade: Optional[str] = None
    quantidade: Optional[float] = None

    # Campos legados mantidos para compatibilidade com dados/API anteriores.
    item_nome: Optional[str] = None
    observacao: Optional[str] = None
    ordem: Optional[int] = None

    @model_validator(mode="after")
    def _validate_material(self) -> "BomItemInput":
        material = (self.material or self.item_nome or "").strip()
        if not material:
            raise ValueError("material da BOM ausente")
        return self


class BomReplaceInput(BaseModel):
    itens: list[BomItemInput]
