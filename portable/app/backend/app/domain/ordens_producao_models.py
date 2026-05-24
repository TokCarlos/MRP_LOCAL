from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


DataEntregaTipo = Literal["DATA", "TEXTO"]
StatusOP = Literal["RASCUNHO", "PLANEJADA", "EM_PRODUCAO", "PAUSADA", "CONCLUIDA", "CANCELADA"]
StatusProcesso = Literal["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "PAUSADO"]


class OrdemProducaoCreate(BaseModel):
    cliente: Optional[str] = None
    obra: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    material: Optional[str] = None
    solicitante: Optional[str] = None
    data_entrega_tipo: DataEntregaTipo = "TEXTO"
    data_entrega_data: Optional[str] = None
    data_entrega_valor: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[StatusOP] = None
    created_by: Optional[str] = None
    empresa_key: Optional[str] = None
    empresa_nome: Optional[str] = None
    ata_key: Optional[str] = None
    ata_nome: Optional[str] = None
    numero_ata: Optional[str] = None


class OrdemProducaoUpdate(BaseModel):
    cliente: Optional[str] = None
    obra: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    material: Optional[str] = None
    solicitante: Optional[str] = None
    data_entrega_tipo: Optional[DataEntregaTipo] = None
    data_entrega_data: Optional[str] = None
    data_entrega_valor: Optional[str] = None
    observacoes: Optional[str] = None
    status: Optional[StatusOP] = None
    empresa_key: Optional[str] = None
    empresa_nome: Optional[str] = None
    ata_key: Optional[str] = None
    ata_nome: Optional[str] = None
    numero_ata: Optional[str] = None


class OrdemProdutoCreate(BaseModel):
    produto_id: int
    quantidade: float = Field(default=1, gt=0)
    quantidade_inauguracao: Optional[float] = None
    material: Optional[str] = None
    observacao: Optional[str] = None


class OrdemProdutoUpdate(BaseModel):
    quantidade: Optional[float] = Field(default=None, gt=0)
    quantidade_inauguracao: Optional[float] = None
    material: Optional[str] = None
    observacao: Optional[str] = None
    ordem_item: Optional[int] = None


class OrdemBomItemUpdate(BaseModel):
    id: int
    cod: Optional[str] = None
    material: Optional[str] = None
    dim1: Optional[str] = None
    dim2: Optional[str] = None
    espessura: Optional[str] = None
    revestimento: Optional[str] = None
    tamanho: Optional[str] = None
    unidade: Optional[str] = None
    quantidade_unitaria: Optional[float] = None
    ordem_item: Optional[int] = None


class OrdemBomUpdate(BaseModel):
    itens: list[OrdemBomItemUpdate]


class OrdemProcessoUpdate(BaseModel):
    quantidade_concluida: Optional[float] = None
    status: Optional[StatusProcesso] = None
    observacao: Optional[str] = None
