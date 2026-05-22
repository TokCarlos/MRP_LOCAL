from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


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
    grupo: BomGrupo
    item_nome: str = Field(min_length=1)
    quantidade: Optional[float] = None
    unidade: Optional[str] = None
    observacao: Optional[str] = None
    ordem: Optional[int] = None


class BomReplaceInput(BaseModel):
    itens: list[BomItemInput]
