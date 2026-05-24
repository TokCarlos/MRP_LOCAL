from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, model_validator


DataEntregaTipo = Literal["DATA", "TEXTO"]
StatusOP = Literal["RASCUNHO", "PLANEJADA", "EM_PRODUCAO", "PAUSADA", "CONCLUIDA", "CANCELADA"]
ProcessoStatus = Literal["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "PAUSADO"]
KanbanStatusDestino = Literal["NAO_INICIADO", "EM_ANDAMENTO", "CONCLUIDO"]


class OrdemProducaoCreate(BaseModel):
    cliente: Optional[str] = None
    obra: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    material: Optional[str] = None
    solicitante: Optional[str] = None
    data_entrega_input: Optional[str] = None
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
    produtos: list[dict[str, Any]] = Field(default_factory=list)
    itens: list[dict[str, Any]] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_data_entrega(self) -> "OrdemProducaoCreate":
        if self.data_entrega_input:
            return self
        if self.data_entrega_tipo == "DATA" and not (self.data_entrega_data or "").strip():
            raise ValueError("data_entrega_data obrigatoria quando data_entrega_tipo = DATA")
        if self.data_entrega_tipo == "TEXTO" and not (self.data_entrega_valor or "").strip():
            self.data_entrega_valor = "NAO DEFINIDO"
        return self


class OrdemProducaoUpdate(BaseModel):
    cliente: Optional[str] = None
    obra: Optional[str] = None
    modelo: Optional[str] = None
    tipo: Optional[str] = None
    material: Optional[str] = None
    solicitante: Optional[str] = None
    data_entrega_input: Optional[str] = None
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
    quantidade: int = Field(default=1, gt=0)
    quantidade_inauguracao: Optional[float] = None
    material: Optional[str] = None
    observacao: Optional[str] = None


class OrdemProdutoUpdate(BaseModel):
    quantidade: Optional[int] = Field(default=None, gt=0)
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
    status: Optional[ProcessoStatus] = None
    observacao: Optional[str] = None


class OrdemKanbanStatusUpdate(BaseModel):
    status_destino: KanbanStatusDestino
    processo_key: Optional[str] = None
    op_produto_id: Optional[int] = None
    observacao: Optional[str] = None


class OrdemKanbanMoverProximo(BaseModel):
    processo_origem: Optional[str] = None
    op_produto_id: Optional[int] = None
    status_destino: KanbanStatusDestino = "NAO_INICIADO"
    observacao: Optional[str] = None


class OrdemKanbanPular(BaseModel):
    processo_origem: Optional[str] = None
    processo_destino: str
    op_produto_id: Optional[int] = None
    status_destino: KanbanStatusDestino = "NAO_INICIADO"
    observacao: Optional[str] = None


class HistoricoEvento(BaseModel):
    entidade: Optional[str] = None
    entidade_id: Optional[int] = None
    acao: str
    detalhe: Optional[str] = None
    dados_antes: Optional[dict[str, Any]] = None
    dados_depois: Optional[dict[str, Any]] = None
    created_by: Optional[str] = None
