from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


BomGrupo = Literal["tubos", "chapas", "insumos"]


class BomItemInput(BaseModel):
    id: Optional[int] = None
    grupo: BomGrupo
    cod: Optional[str] = None
    material: Optional[str] = None
    dim1: Optional[str] = None
    dim2: Optional[str] = None
    espessura: Optional[str] = None
    revestimento: Optional[str] = None
    tamanho: Optional[str] = None
    unidade: Optional[str] = None
    quantidade: Optional[float] = None
    item_nome: Optional[str] = None
    observacao: Optional[str] = None
    ordem: Optional[int] = None


class BomReplaceInput(BaseModel):
    itens: list[BomItemInput]
