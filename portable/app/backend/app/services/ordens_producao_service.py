from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional

from app.repositories.ordens_producao_repository import OrdensProducaoRepository
from app.repositories.produtos_repository import ProdutosRepository

EMPRESA_NOME_BY_KEY = {"jpl": "JPL", "aco": "Aço", "tcr": "TCR"}


PROCESSOS_PADRAO: List[Dict[str, Any]] = [
    {"ordem": 1, "processo_key": "corte", "processo_nome": "Corte"},
    {"ordem": 2, "processo_key": "dobra", "processo_nome": "Dobra"},
    {"ordem": 3, "processo_key": "montagem_solda", "processo_nome": "Montagem Solda"},
    {"ordem": 4, "processo_key": "solda", "processo_nome": "Solda"},
    {"ordem": 5, "processo_key": "acabamento", "processo_nome": "Acabamento"},
    {"ordem": 6, "processo_key": "pintura", "processo_nome": "Pintura"},
    {"ordem": 7, "processo_key": "sublimacao", "processo_nome": "Sublimação"},
    {"ordem": 8, "processo_key": "montagem", "processo_nome": "Montagem"},
    {"ordem": 9, "processo_key": "teste", "processo_nome": "Teste"},
    {"ordem": 10, "processo_key": "expedicao", "processo_nome": "Expedição"},
]

STATUS_OP_VALIDOS = {"RASCUNHO", "PLANEJADA", "EM_PRODUCAO", "PAUSADA", "CONCLUIDA", "CANCELADA"}
STATUS_PROCESSO_VALIDOS = {"PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "PAUSADO"}
DATA_ENTREGA_TIPOS_VALIDOS = {"DATA", "TEXTO"}


class OrdensProducaoService:
    def __init__(self, repository: OrdensProducaoRepository, produtos_repository: ProdutosRepository) -> None:
        self._repository = repository
        self._produtos_repository = produtos_repository

    @staticmethod
    def _text(value: Any) -> Optional[str]:
        if value is None:
            return None
        txt = str(value).strip()
        return txt or None

    @staticmethod
    def _float(value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _format_data_ddmmyyyy(date_str: str) -> str:
        raw = str(date_str).strip()
        if "T" in raw:
            raw = raw.split("T", 1)[0]
        yyyy, mm, dd = raw.split("-")
        return f"{dd}/{mm}/{yyyy}"

    @staticmethod
    def _safe_empresa_nome(empresa_key: Optional[str], fallback: Optional[str] = None) -> str:
        key = (empresa_key or "").strip().lower()
        if key in EMPRESA_NOME_BY_KEY:
            return EMPRESA_NOME_BY_KEY[key]
        return (fallback or "").strip()

    @staticmethod
    def _normalize_empresa_key(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        txt = str(value).strip()
        if not txt:
            return ""
        normalized = txt.lower()
        if normalized in {"aço", "ao", "aco"}:
            normalized = "aco"
        if normalized not in EMPRESA_NOME_BY_KEY:
            raise ValueError("empresa invalida")
        return normalized

    @staticmethod
    def _validate_status_op(status: Optional[str]) -> Optional[str]:
        if status is None:
            return None
        normalized = str(status).strip().upper()
        if normalized not in STATUS_OP_VALIDOS:
            raise ValueError("status da OP invalido")
        return normalized

    @staticmethod
    def _validate_status_processo(status: Optional[str]) -> Optional[str]:
        if status is None:
            return None
        normalized = str(status).strip().upper()
        if normalized not in STATUS_PROCESSO_VALIDOS:
            raise ValueError("status de processo invalido")
        return normalized

    def _normalize_data_entrega(
        self,
        data_entrega_tipo: Optional[str],
        data_entrega_data: Optional[str],
        data_entrega_valor: Optional[str],
    ) -> Dict[str, Optional[str]]:
        tipo = (data_entrega_tipo or "TEXTO").strip().upper()
        if tipo not in DATA_ENTREGA_TIPOS_VALIDOS:
            raise ValueError("data_entrega_tipo invalido")
        if tipo == "DATA":
            raw_date = self._text(data_entrega_data)
            if not raw_date:
                raise ValueError("data_entrega_data obrigatoria quando data_entrega_tipo = DATA")
            try:
                date.fromisoformat(raw_date)
            except ValueError as exc:
                raise ValueError("data_entrega_data invalida. Use YYYY-MM-DD") from exc
            return {
                "data_entrega_tipo": "DATA",
                "data_entrega_data": raw_date,
                "data_entrega_valor": self._text(data_entrega_valor) or self._format_data_ddmmyyyy(raw_date),
            }
        return {
            "data_entrega_tipo": "TEXTO",
            "data_entrega_data": None,
            "data_entrega_valor": self._text(data_entrega_valor) or "NÃO DEFINIDO",
        }

    def _produto_snapshot(self, produto_id: int) -> Optional[Dict[str, Any]]:
        produto = self._produtos_repository.get_produto(produto_id)
        if not produto:
            return None
        contract = produto.to_contract()
        raw = produto.raw
        return {
            "id": contract.get("id"),
            "produto_key": contract.get("produto_key"),
            "item_ata": contract.get("item_ata"),
            "nome_oficial": contract.get("nome_oficial"),
            "imagem_path": contract.get("imagem_path"),
            "empresa_key": contract.get("empresa_key"),
            "empresa_nome": contract.get("empresa_nome") or contract.get("empresa"),
            "ata_key": contract.get("ata_key") or raw.get("ata_key") or raw.get("arp_key"),
            "ata_nome": raw.get("ata_nome") or raw.get("arp"),
            "numero_ata": raw.get("numero_ata") or raw.get("ata_numero"),
            "ativo": bool(contract.get("ativo", True)),
        }

    def list_ordens(self) -> List[Dict[str, Any]]:
        rows = self._repository.list_ordens(include_inactive=False)
        out: List[Dict[str, Any]] = []
        for row in rows:
            out.append(
                {
                    "id": row.get("id"),
                    "numero_op": row.get("numero_op"),
                    "empresa_nome": row.get("empresa_nome"),
                    "cliente": row.get("cliente"),
                    "obra": row.get("obra"),
                    "data_entrega_valor": row.get("data_entrega_valor"),
                    "status": row.get("status"),
                    "total_produtos": int(row.get("total_produtos") or 0),
                    "total_unidades": self._float(row.get("total_unidades"), 0.0),
                    "updated_at": row.get("updated_at"),
                }
            )
        return out

    def get_ordem(self, op_id: int) -> Dict[str, Any]:
        row = self._repository.get_ordem(op_id, include_inactive=False)
        if not row:
            raise ValueError("ordem de producao inexistente")
        produtos = self._repository.list_op_produtos(op_id, include_inactive=False)
        bom = self._repository.list_op_bom(op_id, include_inactive=False)
        processos = self._repository.list_processos(op_id, include_inactive=False)
        produtos_map = {int(item.get("id") or 0): item for item in produtos}
        for item in bom:
            op_produto = produtos_map.get(int(item.get("op_produto_id") or 0), {})
            item["nome_produto"] = op_produto.get("nome_produto")
        for item in processos:
            op_produto = produtos_map.get(int(item.get("op_produto_id") or 0), {})
            item["nome_produto"] = op_produto.get("nome_produto")
        resumo = {
            "total_produtos": int(row.get("total_produtos") or 0),
            "total_unidades": self._float(row.get("total_unidades"), 0.0),
            "total_itens_bom": len(bom),
            "total_processos": len(processos),
        }
        return {"cabecalho": row, "produtos": produtos, "bom": bom, "processos": processos, "resumo": resumo}

    def registrar_historico(
        self,
        op_id: int,
        entidade: Optional[str],
        entidade_id: Optional[int],
        acao: str,
        detalhe: Optional[str],
        dados_antes: Optional[Dict[str, Any]] = None,
        dados_depois: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        return self._repository.registrar_historico(
            op_id=op_id,
            entidade=entidade,
            entidade_id=entidade_id,
            acao=acao,
            detalhe=detalhe,
            dados_antes=dados_antes,
            dados_depois=dados_depois,
            created_by=created_by,
        )

    def create_ordem(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        numero = self._repository.gerar_proximo_numero_op(now.year)
        empresa_key = self._normalize_empresa_key(payload.get("empresa_key"))
        empresa_nome = self._safe_empresa_nome(empresa_key, payload.get("empresa_nome"))
        data_entrega = self._normalize_data_entrega(
            payload.get("data_entrega_tipo"),
            payload.get("data_entrega_data"),
            payload.get("data_entrega_valor"),
        )
        status = self._validate_status_op(payload.get("status")) or "RASCUNHO"
        created = self._repository.create_ordem(
            {
                "numero_op": numero["numero_op"],
                "ano": numero["ano"],
                "seq": numero["seq"],
                "rev": payload.get("rev") or "00",
                "empresa_key": empresa_key or "",
                "empresa_nome": empresa_nome or "",
                "ata_key": self._text(payload.get("ata_key")),
                "ata_nome": self._text(payload.get("ata_nome")),
                "numero_ata": self._text(payload.get("numero_ata")),
                "cliente": self._text(payload.get("cliente")),
                "obra": self._text(payload.get("obra")),
                "modelo": self._text(payload.get("modelo")),
                "tipo": self._text(payload.get("tipo")),
                "material": self._text(payload.get("material")),
                "solicitante": self._text(payload.get("solicitante")),
                "data_entrega_tipo": data_entrega["data_entrega_tipo"],
                "data_entrega_data": data_entrega["data_entrega_data"],
                "data_entrega_valor": data_entrega["data_entrega_valor"],
                "status": status,
                "observacoes": self._text(payload.get("observacoes")),
                "created_by": self._text(payload.get("created_by")),
            }
        )
        self.registrar_historico(
            op_id=int(created["id"]),
            entidade="OP",
            entidade_id=int(created["id"]),
            acao="OP_CRIADA",
            detalhe=f"OP {created.get('numero_op')} criada.",
            dados_depois={"numero_op": created.get("numero_op"), "status": created.get("status")},
            created_by=self._text(payload.get("created_by")),
        )
        return created

    def update_ordem(self, op_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        current = self._repository.get_ordem(op_id, include_inactive=False)
        if not current:
            raise ValueError("ordem de producao inexistente")
        updates: Dict[str, Any] = {}
        for field in ("cliente", "obra", "modelo", "tipo", "material", "solicitante", "observacoes", "ata_key", "ata_nome", "numero_ata"):
            if field in payload:
                updates[field] = self._text(payload.get(field))
        if "empresa_key" in payload:
            empresa_key = self._normalize_empresa_key(payload.get("empresa_key"))
            updates["empresa_key"] = empresa_key or ""
            updates["empresa_nome"] = self._safe_empresa_nome(empresa_key, payload.get("empresa_nome") or current.get("empresa_nome"))
        elif "empresa_nome" in payload:
            updates["empresa_nome"] = self._text(payload.get("empresa_nome")) or ""
        status_before = str(current.get("status") or "").upper()
        status_after = status_before
        if "status" in payload:
            status_after = self._validate_status_op(payload.get("status")) or status_before
            updates["status"] = status_after
        if {"data_entrega_tipo", "data_entrega_data", "data_entrega_valor"} & set(payload.keys()):
            updates.update(
                self._normalize_data_entrega(
                    payload.get("data_entrega_tipo", current.get("data_entrega_tipo")),
                    payload.get("data_entrega_data", current.get("data_entrega_data")),
                    payload.get("data_entrega_valor", current.get("data_entrega_valor")),
                )
            )
        updated = self._repository.update_ordem(op_id, updates)
        if not updated:
            raise ValueError("ordem de producao inexistente")
        self.registrar_historico(op_id, "OP", op_id, "OP_EDITADA", "Cabeçalho da OP atualizado.", current, updated)
        if status_after != status_before:
            self.registrar_historico(
                op_id,
                "OP",
                op_id,
                "STATUS_ALTERADO",
                f"Status alterado de {status_before} para {status_after}.",
                {"status": status_before},
                {"status": status_after},
            )
        return updated

    def delete_ordem(self, op_id: int) -> Dict[str, Any]:
        current = self._repository.get_ordem(op_id, include_inactive=False)
        if not current:
            raise ValueError("ordem de producao inexistente")
        ok = self._repository.soft_delete_ordem(op_id)
        self.registrar_historico(
            op_id, "OP", op_id, "STATUS_ALTERADO", "OP cancelada e removida da listagem ativa.",
            {"status": current.get("status"), "ativo": current.get("ativo")},
            {"status": "CANCELADA", "ativo": 0},
        )
        return {"inativada": bool(ok)}

    def _validar_regra_ata_regente(self, op: Dict[str, Any], produto: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        produto_empresa_key = self._text(produto.get("empresa_key"))
        produto_ata_key = self._text(produto.get("ata_key"))
        if not produto_ata_key:
            raise ValueError("produto sem ATA vinculada. Inclusao bloqueada nesta OP.")
        op_empresa_key = self._text(op.get("empresa_key"))
        op_ata_key = self._text(op.get("ata_key"))
        if op_empresa_key and op_ata_key:
            if op_empresa_key != produto_empresa_key or op_ata_key != produto_ata_key:
                raise ValueError("Produto pertence a outra empresa/ATA regente e não pode ser incluído nesta OP.")
            return None
        return {
            "empresa_key": produto_empresa_key or "",
            "empresa_nome": self._safe_empresa_nome(produto_empresa_key, produto.get("empresa_nome")),
            "ata_key": produto_ata_key,
            "ata_nome": self._text(produto.get("ata_nome")),
            "numero_ata": self._text(produto.get("numero_ata")),
        }

    def list_op_produtos(self, op_id: int) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        return self._repository.list_op_produtos(op_id, include_inactive=False)

    def add_op_produto(self, op_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        op = self._repository.get_ordem(op_id, include_inactive=False)
        if not op:
            raise ValueError("ordem de producao inexistente")
        produto_id = int(payload.get("produto_id") or 0)
        if produto_id <= 0:
            raise ValueError("produto_id invalido")
        quantidade = self._float(payload.get("quantidade"), 0.0)
        if quantidade <= 0:
            raise ValueError("quantidade deve ser maior que zero")

        produto = self._produto_snapshot(produto_id)
        if not produto or not bool(produto.get("ativo", True)):
            raise ValueError("produto inexistente")

        regente_update = self._validar_regra_ata_regente(op, produto)
        if regente_update:
            self._repository.update_ordem(op_id, regente_update)

        ordem_item = len(self._repository.list_op_produtos(op_id, include_inactive=False)) + 1
        op_produto = self._repository.create_op_produto(
            {
                "op_id": op_id,
                "produto_id": produto_id,
                "produto_key": self._text(produto.get("produto_key")),
                "item_ata": self._text(produto.get("item_ata")),
                "nome_produto": self._text(produto.get("nome_oficial")),
                "empresa_key": self._text(produto.get("empresa_key")),
                "empresa_nome": self._safe_empresa_nome(produto.get("empresa_key"), produto.get("empresa_nome")),
                "ata_key": self._text(produto.get("ata_key")),
                "ata_nome": self._text(produto.get("ata_nome")),
                "numero_ata": self._text(produto.get("numero_ata")),
                "imagem_path": self._text(produto.get("imagem_path")),
                "quantidade": quantidade,
                "quantidade_inauguracao": payload.get("quantidade_inauguracao"),
                "material": self._text(payload.get("material")),
                "ordem_item": ordem_item,
                "observacao": self._text(payload.get("observacao")),
            }
        )
        bom_rows = self._produtos_repository.list_bom(produto_id)
        self._repository.create_op_bom_from_snapshot(op_id, int(op_produto["id"]), produto_id, quantidade, bom_rows)
        self._repository.create_processos_padrao(op_id, int(op_produto["id"]), quantidade, PROCESSOS_PADRAO)
        self.registrar_historico(
            op_id, "OP_PRODUTO", int(op_produto["id"]), "PRODUTO_ADICIONADO",
            f"Produto {op_produto.get('produto_key')} adicionado a OP.",
            None,
            {"produto_id": produto_id, "produto_key": op_produto.get("produto_key"), "quantidade": quantidade},
        )
        return op_produto

    def update_op_produto(self, op_id: int, op_produto_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        current = self._repository.get_op_produto(op_id, op_produto_id, include_inactive=False)
        if not current:
            raise ValueError("produto da OP inexistente")
        updates: Dict[str, Any] = {}
        before = self._float(current.get("quantidade"), 0.0)
        after = before
        if "quantidade" in payload and payload.get("quantidade") is not None:
            after = self._float(payload.get("quantidade"), 0.0)
            if after <= 0:
                raise ValueError("quantidade deve ser maior que zero")
            updates["quantidade"] = after
        for field in ("quantidade_inauguracao", "material", "observacao", "ordem_item"):
            if field in payload:
                updates[field] = payload.get(field)
        updated = self._repository.update_op_produto(op_id, op_produto_id, updates)
        if not updated:
            raise ValueError("produto da OP inexistente")
        if after != before:
            self._repository.recalc_bom_quantidades(op_id, op_produto_id, after)
            self._repository.recalc_processos_planejamento(op_id, op_produto_id, after)
            self.registrar_historico(
                op_id, "OP_PRODUTO", op_produto_id, "QUANTIDADE_ALTERADA",
                "Quantidade do produto na OP alterada.",
                {"quantidade": before},
                {"quantidade": after},
            )
        return updated

    def remove_op_produto(self, op_id: int, op_produto_id: int) -> Dict[str, Any]:
        current = self._repository.get_op_produto(op_id, op_produto_id, include_inactive=False)
        if not current:
            raise ValueError("produto da OP inexistente")
        ok = self._repository.soft_delete_op_produto(op_id, op_produto_id)
        self._repository.soft_delete_op_bom_by_produto(op_id, op_produto_id)
        self._repository.soft_delete_processos_by_produto(op_id, op_produto_id)
        self.registrar_historico(
            op_id, "OP_PRODUTO", op_produto_id, "PRODUTO_REMOVIDO",
            f"Produto {current.get('produto_key')} removido da OP.",
            {"produto_key": current.get("produto_key"), "quantidade": current.get("quantidade")},
            None,
        )
        return {"inativado": bool(ok)}

    def list_bom(self, op_id: int) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        rows = self._repository.list_op_bom(op_id, include_inactive=False)
        produtos = self._repository.list_op_produtos(op_id, include_inactive=False)
        by_id = {int(item.get("id") or 0): item for item in produtos}
        for row in rows:
            row["nome_produto"] = by_id.get(int(row.get("op_produto_id") or 0), {}).get("nome_produto")
        return rows

    def update_bom(self, op_id: int, itens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        payload: List[Dict[str, Any]] = []
        for item in itens:
            bom_id = int(item.get("id") or 0)
            if bom_id <= 0:
                continue
            normalized: Dict[str, Any] = {"id": bom_id}
            for key in ("cod", "material", "dim1", "dim2", "espessura", "revestimento", "tamanho", "unidade", "ordem_item"):
                if key in item:
                    normalized[key] = self._text(item.get(key))
            if "quantidade_unitaria" in item:
                normalized["quantidade_unitaria"] = self._float(item.get("quantidade_unitaria"), 0.0)
            payload.append(normalized)
        rows = self._repository.update_op_bom_items(op_id, payload)
        self.registrar_historico(
            op_id, "OP_BOM", None, "BOM_OP_EDITADA",
            f"BOM operacional da OP atualizada ({len(payload)} item(ns)).",
            None,
            {"itens_editados": len(payload)},
        )
        return rows

    def list_processos(self, op_id: int) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        rows = self._repository.list_processos(op_id, include_inactive=False)
        produtos = self._repository.list_op_produtos(op_id, include_inactive=False)
        by_id = {int(item.get("id") or 0): item for item in produtos}
        for row in rows:
            row["nome_produto"] = by_id.get(int(row.get("op_produto_id") or 0), {}).get("nome_produto")
        return rows

    def update_processo(self, op_id: int, processo_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        current = self._repository.get_processo(op_id, processo_id)
        if not current:
            raise ValueError("processo inexistente")
        updates: Dict[str, Any] = {}
        if "quantidade_concluida" in payload and payload.get("quantidade_concluida") is not None:
            qtd = self._float(payload.get("quantidade_concluida"), -1.0)
            if qtd < 0:
                raise ValueError("quantidade_concluida invalida")
            updates["quantidade_concluida"] = qtd
        if "status" in payload:
            updates["status"] = self._validate_status_processo(payload.get("status"))
        if "observacao" in payload:
            updates["observacao"] = self._text(payload.get("observacao"))
        updated = self._repository.update_processo(op_id, processo_id, updates)
        if not updated:
            raise ValueError("processo inexistente")
        self.registrar_historico(
            op_id, "OP_PROCESSO", processo_id, "PROCESSO_ATUALIZADO",
            f"Processo {updated.get('processo_nome')} atualizado.",
            current,
            updated,
        )
        return updated

    def list_historico(self, op_id: int) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        return self._repository.list_historico(op_id)
