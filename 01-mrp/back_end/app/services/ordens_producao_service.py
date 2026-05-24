from __future__ import annotations

from datetime import date, datetime, timezone
import re
import unicodedata
from typing import Any, Dict, List, Optional

from app.core.normalize import EMPRESA_NOME_BY_KEY, normalize_empresa_key
from app.repositories.ordens_producao_repository import OrdensProducaoRepository


PROCESSOS_PADRAO: List[Dict[str, Any]] = [
    {"ordem": 1, "processo_key": "corte", "processo_nome": "Corte"},
    {"ordem": 2, "processo_key": "dobra", "processo_nome": "Dobra"},
    {"ordem": 3, "processo_key": "montagem_solda", "processo_nome": "Montagem Solda"},
    {"ordem": 4, "processo_key": "solda", "processo_nome": "Soldagem"},
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
STATUS_KANBAN_VALIDOS = {"NAO_INICIADO", "EM_ANDAMENTO", "CONCLUIDO"}
STATUS_KANBAN_NOMES = {
    "NAO_INICIADO": "Não Iniciado",
    "EM_ANDAMENTO": "Em Andamento",
    "CONCLUIDO": "Concluído",
}
PROCESSOS_CANONICOS = {item["processo_key"]: item for item in PROCESSOS_PADRAO}


class OrdensProducaoService:
    def __init__(self, repository: OrdensProducaoRepository) -> None:
        self._repository = repository

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
    def _positive_int(value: Any, field_name: str = "quantidade") -> int:
        if isinstance(value, bool) or value is None:
            raise ValueError(f"{field_name} deve ser um número inteiro maior que zero")
        if isinstance(value, int):
            parsed = value
        elif isinstance(value, float):
            if not value.is_integer():
                raise ValueError(f"{field_name} deve ser um número inteiro maior que zero")
            parsed = int(value)
        else:
            raw = str(value).strip()
            if not re.fullmatch(r"\d+", raw):
                raise ValueError(f"{field_name} deve ser um número inteiro maior que zero")
            parsed = int(raw)
        if parsed <= 0:
            raise ValueError(f"{field_name} deve ser um número inteiro maior que zero")
        return parsed

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
        return normalize_empresa_key(txt)

    @staticmethod
    def _upper_texto_operacional(value: Optional[str]) -> str:
        txt = str(value or "").strip()
        txt = re.sub(r"\s+", " ", txt)
        return txt.upper() if txt else "NÃO DEFINIDO"

    @staticmethod
    def _ascii_upper(value: Optional[str]) -> str:
        raw = str(value or "").strip().upper()
        raw = unicodedata.normalize("NFD", raw)
        return "".join(ch for ch in raw if unicodedata.category(ch) != "Mn")

    def _normalize_data_entrega_input(self, value: Optional[str]) -> Optional[Dict[str, Optional[str]]]:
        raw = self._text(value)
        if not raw:
            return {"data_entrega_tipo": "TEXTO", "data_entrega_data": None, "data_entrega_valor": "NÃO DEFINIDO"}
        match = re.fullmatch(r"\s*(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2}|\d{4})\s*", raw)
        if match:
            dd = int(match.group(1))
            mm = int(match.group(2))
            yy_raw = match.group(3)
            yyyy = int(yy_raw) if len(yy_raw) == 4 else 2000 + int(yy_raw)
            try:
                parsed = date(yyyy, mm, dd)
            except ValueError as exc:
                raise ValueError("data_entrega_input invalida") from exc
            return {
                "data_entrega_tipo": "DATA",
                "data_entrega_data": parsed.isoformat(),
                "data_entrega_valor": parsed.strftime("%d/%m/%Y"),
            }
        normalized_ascii = self._ascii_upper(raw)
        aliases = {
            "NAO DEFINIDO": "NÃO DEFINIDO",
            "NÃO DEFINIDO": "NÃO DEFINIDO",
            "A DEFINIR": "A DEFINIR",
            "URGENTE": "URGENTE",
            "SEM DATA": "SEM DATA",
            "AGUARDANDO CLIENTE": "AGUARDANDO CLIENTE",
        }
        valor = aliases.get(normalized_ascii, self._upper_texto_operacional(raw))
        return {"data_entrega_tipo": "TEXTO", "data_entrega_data": None, "data_entrega_valor": valor}

    def _normalize_data_entrega(
        self,
        data_entrega_tipo: Optional[str],
        data_entrega_data: Optional[str],
        data_entrega_valor: Optional[str],
        data_entrega_input: Optional[str] = None,
    ) -> Dict[str, Optional[str]]:
        if data_entrega_input is not None:
            return self._normalize_data_entrega_input(data_entrega_input) or {
                "data_entrega_tipo": "TEXTO", "data_entrega_data": None, "data_entrega_valor": "NÃO DEFINIDO"
            }
        tipo = (data_entrega_tipo or "TEXTO").strip().upper()
        if tipo not in DATA_ENTREGA_TIPOS_VALIDOS:
            raise ValueError("data_entrega_tipo invalido")
        if tipo == "DATA":
            raw_date = self._text(data_entrega_data)
            if not raw_date:
                fallback = self._normalize_data_entrega_input(data_entrega_valor)
                if fallback and fallback["data_entrega_tipo"] == "DATA":
                    return fallback
                raise ValueError("data_entrega_data obrigatoria quando data_entrega_tipo = DATA")
            try:
                parsed = date.fromisoformat(raw_date)
            except ValueError as exc:
                raise ValueError("data_entrega_data invalida. Use YYYY-MM-DD") from exc
            valor = self._text(data_entrega_valor) or parsed.strftime("%d/%m/%Y")
            return {"data_entrega_tipo": "DATA", "data_entrega_data": parsed.isoformat(), "data_entrega_valor": valor}
        valor_texto = self._normalize_data_entrega_input(data_entrega_valor)
        return valor_texto or {"data_entrega_tipo": "TEXTO", "data_entrega_data": None, "data_entrega_valor": "NÃO DEFINIDO"}

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

    @staticmethod
    def _normalize_status_kanban(value: Optional[str]) -> str:
        raw = str(value or "").strip().upper()
        raw = raw.replace(" ", "_").replace("-", "_")
        raw = raw.replace("CONCLUÍDO", "CONCLUIDO")
        if raw in {"NAO_INICIADO", "NÃO_INICIADO", "PENDENTE"}:
            return "NAO_INICIADO"
        if raw in {"EM_ANDAMENTO", "PAUSADO"}:
            return "EM_ANDAMENTO"
        if raw in {"CONCLUIDO"}:
            return "CONCLUIDO"
        return "NAO_INICIADO"

    @staticmethod
    def _status_kanban_para_db(status_kanban: str) -> str:
        if status_kanban == "CONCLUIDO":
            return "CONCLUIDO"
        if status_kanban == "EM_ANDAMENTO":
            return "EM_ANDAMENTO"
        return "PENDENTE"

    def _prazo_info(self, row: Dict[str, Any]) -> Dict[str, str]:
        tipo = str(row.get("data_entrega_tipo") or "").strip().upper()
        raw_data = self._text(row.get("data_entrega_data"))
        if tipo != "DATA" or not raw_data:
            return {"prazo_label": "", "prazo_status": "indefinido"}
        try:
            target = date.fromisoformat(raw_data.split("T", 1)[0])
        except ValueError:
            return {"prazo_label": "", "prazo_status": "indefinido"}

        diff = (target - date.today()).days
        if diff > 0:
            return {"prazo_label": f"Faltam {diff} dias", "prazo_status": "ok"}
        if diff == 0:
            return {"prazo_label": "Hoje", "prazo_status": "hoje"}
        return {"prazo_label": f"Atrasado {abs(diff)} dias", "prazo_status": "atrasado"}

    def _macro_from_processos(self, processos: List[Dict[str, Any]]) -> Dict[str, Any]:
        default_macro = {
            "processo_macro_key": "corte",
            "processo_macro_nome": PROCESSOS_CANONICOS["corte"]["processo_nome"],
            "processo_macro_ordem": 1,
            "status_processo_macro": "NAO_INICIADO",
            "rows_macro": [],
            "rows_all": [],
        }
        if not processos:
            return default_macro

        normalized_rows: List[Dict[str, Any]] = []
        for row in processos:
            processo_key = str(row.get("processo_key") or "").strip().lower()
            canonical = PROCESSOS_CANONICOS.get(processo_key)
            if not canonical:
                continue
            item = dict(row)
            item["_processo_key"] = processo_key
            item["_processo_ordem"] = int(canonical["ordem"])
            item["_processo_nome"] = str(canonical["processo_nome"])
            item["_status_kanban"] = self._normalize_status_kanban(row.get("status"))
            normalized_rows.append(item)

        if not normalized_rows:
            return default_macro

        pending = [row for row in normalized_rows if row["_status_kanban"] != "CONCLUIDO"]
        if pending:
            menor_ordem = min(int(row["_processo_ordem"]) for row in pending)
            rows_macro = [row for row in pending if int(row["_processo_ordem"]) == menor_ordem]
            status_macro = (
                "NAO_INICIADO"
                if any(row["_status_kanban"] == "NAO_INICIADO" for row in rows_macro)
                else "EM_ANDAMENTO"
            )
            first = rows_macro[0]
            return {
                "processo_macro_key": first["_processo_key"],
                "processo_macro_nome": first["_processo_nome"],
                "processo_macro_ordem": int(first["_processo_ordem"]),
                "status_processo_macro": status_macro,
                "rows_macro": rows_macro,
                "rows_all": normalized_rows,
            }

        exp_rows = [row for row in normalized_rows if row["_processo_key"] == "expedicao"]
        chosen = exp_rows[0] if exp_rows else max(normalized_rows, key=lambda row: int(row["_processo_ordem"]))
        rows_macro = [row for row in normalized_rows if row["_processo_key"] == chosen["_processo_key"]]
        return {
            "processo_macro_key": chosen["_processo_key"],
            "processo_macro_nome": chosen["_processo_nome"],
            "processo_macro_ordem": int(chosen["_processo_ordem"]),
            "status_processo_macro": "CONCLUIDO",
            "rows_macro": rows_macro,
            "rows_all": normalized_rows,
        }

    def _apply_status_to_processo(
        self,
        op_id: int,
        row: Dict[str, Any],
        status_kanban: str,
        observacao: Optional[str] = None,
    ) -> Dict[str, Any]:
        status = self._normalize_status_kanban(status_kanban)
        planejada = self._float(row.get("quantidade_planejada"), 0.0)
        concluida_atual = self._float(row.get("quantidade_concluida"), 0.0)
        if status == "CONCLUIDO":
            concluida_destino = planejada
        elif status == "NAO_INICIADO":
            concluida_destino = 0.0
        else:
            concluida_destino = max(min(concluida_atual, planejada), 0.0)

        payload = {
            "status": self._status_kanban_para_db(status),
            "quantidade_concluida": concluida_destino,
        }
        if observacao is not None:
            payload["observacao"] = observacao

        updated = self._repository.update_processo(op_id, int(row["id"]), payload)
        if not updated:
            raise ValueError("falha ao atualizar processo da OP")
        return updated

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

    def list_kanban(self) -> Dict[str, Any]:
        ordens = self._repository.list_ordens(include_inactive=False)
        processos_all = self._repository.list_processos_all_ordens()

        processos_por_op: Dict[int, List[Dict[str, Any]]] = {}
        for row in processos_all:
            op_id = int(row.get("op_id") or 0)
            if op_id <= 0:
                continue
            processos_por_op.setdefault(op_id, []).append(row)

        board: List[Dict[str, Any]] = []
        board_index: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
        for processo in PROCESSOS_PADRAO:
            status_rows = [
                {"status_key": "NAO_INICIADO", "status_nome": STATUS_KANBAN_NOMES["NAO_INICIADO"], "ordens": []},
                {"status_key": "EM_ANDAMENTO", "status_nome": STATUS_KANBAN_NOMES["EM_ANDAMENTO"], "ordens": []},
                {"status_key": "CONCLUIDO", "status_nome": STATUS_KANBAN_NOMES["CONCLUIDO"], "ordens": []},
            ]
            board.append(
                {
                    "processo_key": processo["processo_key"],
                    "processo_nome": processo["processo_nome"],
                    "ordem": int(processo["ordem"]),
                    "status": status_rows,
                }
            )
            board_index[processo["processo_key"]] = {entry["status_key"]: entry["ordens"] for entry in status_rows}

        for ordem in ordens:
            op_id = int(ordem.get("id") or 0)
            macro = self._macro_from_processos(processos_por_op.get(op_id, []))
            prazo = self._prazo_info(ordem)
            status_macro = self._normalize_status_kanban(macro["status_processo_macro"])
            processo_macro_key = str(macro["processo_macro_key"])
            if processo_macro_key not in board_index:
                processo_macro_key = "corte"
                status_macro = "NAO_INICIADO"
                macro_nome = PROCESSOS_CANONICOS["corte"]["processo_nome"]
                macro_ordem = 1
            else:
                macro_nome = str(macro["processo_macro_nome"])
                macro_ordem = int(macro["processo_macro_ordem"])

            card = {
                "id": op_id,
                "numero_op": ordem.get("numero_op"),
                "cliente": ordem.get("cliente"),
                "obra": ordem.get("obra"),
                "data_entrega_tipo": ordem.get("data_entrega_tipo"),
                "data_entrega_data": ordem.get("data_entrega_data"),
                "data_entrega_valor": ordem.get("data_entrega_valor"),
                "prazo_label": prazo["prazo_label"],
                "prazo_status": prazo["prazo_status"],
                "processo_macro_key": processo_macro_key,
                "processo_macro_nome": macro_nome,
                "processo_macro_ordem": macro_ordem,
                "status_processo_macro": status_macro,
                "updated_at": ordem.get("updated_at"),
                "empresa_nome": ordem.get("empresa_nome"),
                "status_op": ordem.get("status"),
            }
            board_index[processo_macro_key][status_macro].append(card)

        for processo in board:
            for status_row in processo["status"]:
                status_row["ordens"] = sorted(
                    status_row["ordens"],
                    key=lambda item: str(item.get("updated_at") or ""),
                    reverse=True,
                )

        return {"processos": board}

    def get_ordem(self, op_id: int) -> Dict[str, Any]:
        row = self._repository.get_ordem(op_id, include_inactive=False)
        if not row:
            raise ValueError("ordem de producao inexistente")
        produtos = self._repository.list_op_produtos(op_id, include_inactive=False)
        bom = self._repository.list_op_bom(op_id, include_inactive=False)
        processos = self._repository.list_processos(op_id, include_inactive=False)
        resumo = {
            "total_produtos": int(row.get("total_produtos") or 0),
            "total_unidades": self._float(row.get("total_unidades"), 0.0),
            "total_itens_bom": len(bom),
            "total_processos": len(processos),
        }
        return {
            "cabecalho": row,
            "produtos": produtos,
            "bom": bom,
            "processos": processos,
            "resumo": resumo,
        }

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
        produtos_raw = payload.get("produtos") or payload.get("itens") or []
        if produtos_raw is None:
            produtos_raw = []
        if not isinstance(produtos_raw, list):
            raise ValueError("produtos da OP devem ser uma lista")

        ata_key_payload = self._text(payload.get("ata_key"))
        ata_key_norm = (ata_key_payload or "").strip().lower()
        is_especial = ata_key_norm == "especial"

        produtos_payloads: List[Dict[str, Any]] = []
        ata_ref: Optional[Dict[str, Any]] = None
        for raw_item in produtos_raw:
            if not isinstance(raw_item, dict):
                raise ValueError("item de produto invalido na OP")
            produto_id = int(raw_item.get("produto_id") or raw_item.get("id") or 0)
            if produto_id <= 0:
                raise ValueError("produto_id invalido na criacao da OP")
            quantidade = self._positive_int(raw_item.get("quantidade"), "quantidade do produto")

            produto = self._repository.get_produto_snapshot(produto_id)
            if not produto or not int(produto.get("ativo") or 0):
                raise ValueError(f"produto inexistente ou inativo: {produto_id}")
            produto_ata_key = self._text(produto.get("ata_key"))
            if not produto_ata_key:
                raise ValueError("produto sem ATA vinculada. Inclusao bloqueada nesta OP.")
            if ata_key_norm and not is_especial and produto_ata_key != ata_key_norm:
                raise ValueError("Produto pertence a outra ATA e não pode ser incluído nesta OP.")
            if ata_ref is None:
                ata_ref = produto
            bom_rows = self._repository.list_produto_bom(produto_id)
            produtos_payloads.append(
                {
                    "produto": produto,
                    "bom_rows": bom_rows,
                    "quantidade": quantidade,
                    "quantidade_inauguracao": raw_item.get("quantidade_inauguracao"),
                    "material": self._text(raw_item.get("material")),
                    "observacao": self._text(raw_item.get("observacao")),
                }
            )

        empresa_key = self._normalize_empresa_key(payload.get("empresa_key"))
        empresa_nome = self._safe_empresa_nome(empresa_key, payload.get("empresa_nome"))
        ata_key = self._text(payload.get("ata_key"))
        ata_nome = self._text(payload.get("ata_nome"))
        numero_ata = self._text(payload.get("numero_ata"))
        if is_especial:
            empresa_key = "especial"
            empresa_nome = "ESPECIAL"
            ata_key = "especial"
            ata_nome = "ESPECIAL"
            numero_ata = "ESPECIAL"
        elif ata_ref is not None:
            empresa_key = self._text(ata_ref.get("empresa_key")) or empresa_key
            empresa_nome = self._safe_empresa_nome(empresa_key, ata_ref.get("empresa_nome"))
            ata_key = self._text(ata_ref.get("ata_key")) or ata_key
            ata_nome = self._text(ata_ref.get("ata_nome")) or ata_nome
            numero_ata = self._text(ata_ref.get("numero_ata")) or numero_ata

        data_entrega = self._normalize_data_entrega(
            payload.get("data_entrega_tipo"),
            payload.get("data_entrega_data"),
            payload.get("data_entrega_valor"),
            payload.get("data_entrega_input"),
        )
        status = self._validate_status_op(payload.get("status")) or "RASCUNHO"
        create_payload = {
            "ano": now.year,
            "rev": payload.get("rev") or "00",
            "empresa_key": empresa_key or "",
            "empresa_nome": empresa_nome or "",
            "ata_key": ata_key,
            "ata_nome": ata_nome,
            "numero_ata": numero_ata,
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
        return self._repository.create_ordem_completa(create_payload, produtos_payloads, PROCESSOS_PADRAO)

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
            if "empresa_nome" in payload:
                updates["empresa_nome"] = self._safe_empresa_nome(empresa_key, payload.get("empresa_nome"))
            else:
                updates["empresa_nome"] = self._safe_empresa_nome(empresa_key, current.get("empresa_nome"))
        elif "empresa_nome" in payload:
            updates["empresa_nome"] = self._text(payload.get("empresa_nome")) or ""

        status_before = str(current.get("status") or "").upper()
        status_after = status_before
        if "status" in payload:
            status_after = self._validate_status_op(payload.get("status")) or status_before
            updates["status"] = status_after

        if {"data_entrega_tipo", "data_entrega_data", "data_entrega_valor", "data_entrega_input"} & set(payload.keys()):
            data_entrega = self._normalize_data_entrega(
                payload.get("data_entrega_tipo", current.get("data_entrega_tipo")),
                payload.get("data_entrega_data", current.get("data_entrega_data")),
                payload.get("data_entrega_valor", current.get("data_entrega_valor")),
                payload.get("data_entrega_input"),
            )
            updates.update(data_entrega)

        updated = self._repository.update_ordem(op_id, updates) or {}
        self.registrar_historico(
            op_id=op_id,
            entidade="OP",
            entidade_id=op_id,
            acao="OP_EDITADA",
            detalhe="Cabeçalho da OP atualizado.",
            dados_antes=current,
            dados_depois=updated,
        )
        if status_after != status_before:
            self.registrar_historico(
                op_id=op_id,
                entidade="OP",
                entidade_id=op_id,
                acao="STATUS_ALTERADO",
                detalhe=f"Status alterado de {status_before} para {status_after}.",
                dados_antes={"status": status_before},
                dados_depois={"status": status_after},
            )
        return updated

    def delete_ordem(self, op_id: int) -> Dict[str, Any]:
        current = self._repository.get_ordem(op_id, include_inactive=False)
        if not current:
            raise ValueError("ordem de producao inexistente")
        deleted = self._repository.soft_delete_ordem(op_id)
        self.registrar_historico(
            op_id=op_id,
            entidade="OP",
            entidade_id=op_id,
            acao="STATUS_ALTERADO",
            detalhe="OP cancelada e removida da listagem ativa.",
            dados_antes={"status": current.get("status"), "ativo": current.get("ativo")},
            dados_depois={"status": "CANCELADA", "ativo": 0},
        )
        return {"inativada": bool(deleted)}

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
        quantidade = self._positive_int(payload.get("quantidade"), "quantidade")

        produto = self._repository.get_produto_snapshot(produto_id)
        if not produto or not int(produto.get("ativo") or 0):
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

        bom_rows = self._repository.list_produto_bom(produto_id)
        self._repository.create_op_bom_from_snapshot(
            op_id=op_id,
            op_produto_id=int(op_produto["id"]),
            produto_id=produto_id,
            quantidade_produto=quantidade,
            bom_rows=bom_rows,
        )
        self._repository.create_processos_padrao(
            op_id=op_id,
            op_produto_id=int(op_produto["id"]),
            quantidade_planejada=quantidade,
            processos=PROCESSOS_PADRAO,
        )
        self.registrar_historico(
            op_id=op_id,
            entidade="OP_PRODUTO",
            entidade_id=int(op_produto["id"]),
            acao="PRODUTO_ADICIONADO",
            detalhe=f"Produto {op_produto.get('produto_key')} adicionado a OP.",
            dados_depois={
                "produto_id": produto_id,
                "produto_key": op_produto.get("produto_key"),
                "quantidade": quantidade,
            },
        )
        return op_produto

    def update_op_produto(self, op_id: int, op_produto_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        current = self._repository.get_op_produto(op_id, op_produto_id, include_inactive=False)
        if not current:
            raise ValueError("produto da OP inexistente")

        updates: Dict[str, Any] = {}
        quantidade_before = self._float(current.get("quantidade"), 0)
        quantidade_after = quantidade_before
        if "quantidade" in payload and payload.get("quantidade") is not None:
            quantidade_after = self._positive_int(payload.get("quantidade"), "quantidade")
            updates["quantidade"] = quantidade_after
        for field in ("quantidade_inauguracao", "material", "observacao", "ordem_item"):
            if field in payload:
                updates[field] = payload.get(field)

        updated = self._repository.update_op_produto(op_id, op_produto_id, updates)
        if not updated:
            raise ValueError("produto da OP inexistente")

        if quantidade_after != quantidade_before:
            self._repository.recalc_bom_quantidades(op_id, op_produto_id, quantidade_after)
            self._repository.recalc_processos_planejamento(op_id, op_produto_id, quantidade_after)
            self.registrar_historico(
                op_id=op_id,
                entidade="OP_PRODUTO",
                entidade_id=op_produto_id,
                acao="QUANTIDADE_ALTERADA",
                detalhe="Quantidade do produto na OP alterada.",
                dados_antes={"quantidade": quantidade_before},
                dados_depois={"quantidade": quantidade_after},
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
            op_id=op_id,
            entidade="OP_PRODUTO",
            entidade_id=op_produto_id,
            acao="PRODUTO_REMOVIDO",
            detalhe=f"Produto {current.get('produto_key')} removido da OP.",
            dados_antes={"produto_key": current.get("produto_key"), "quantidade": current.get("quantidade")},
        )
        return {"inativado": bool(ok)}

    def list_bom(self, op_id: int) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        return self._repository.list_op_bom(op_id, include_inactive=False)

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
            op_id=op_id,
            entidade="OP_BOM",
            entidade_id=None,
            acao="BOM_OP_EDITADA",
            detalhe=f"BOM operacional da OP atualizada ({len(payload)} item(ns)).",
            dados_depois={"itens_editados": len(payload)},
        )
        return rows

    def list_processos(self, op_id: int) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        return self._repository.list_processos(op_id, include_inactive=False)

    def set_kanban_status(self, op_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")

        status_destino = self._normalize_status_kanban(payload.get("status_destino"))
        if status_destino not in STATUS_KANBAN_VALIDOS:
            raise ValueError("status_destino invalido para Kanban")

        processos = self._repository.list_processos(op_id, include_inactive=False)
        macro = self._macro_from_processos(processos)
        processo_key = self._text(payload.get("processo_key")) or str(macro["processo_macro_key"])
        processo_key = processo_key.strip().lower()
        if processo_key not in PROCESSOS_CANONICOS:
            raise ValueError("processo_key invalido")

        op_produto_id = payload.get("op_produto_id")
        op_produto_id = int(op_produto_id) if op_produto_id not in (None, "") else None
        observacao = self._text(payload.get("observacao"))

        rows_target = [
            row
            for row in macro["rows_all"]
            if str(row.get("_processo_key")) == processo_key
            and (op_produto_id is None or int(row.get("op_produto_id") or 0) == op_produto_id)
        ]
        if not rows_target:
            raise ValueError("processo alvo nao encontrado para atualizacao")

        atualizados: List[int] = []
        for row in rows_target:
            updated = self._apply_status_to_processo(op_id, row, status_destino, observacao)
            atualizados.append(int(updated.get("id") or 0))

        self.registrar_historico(
            op_id=op_id,
            entidade="OP_PROCESSO",
            entidade_id=None,
            acao="KANBAN_STATUS_ALTERADO",
            detalhe=(
                f"Kanban: processo {processo_key} marcado como {status_destino}"
                f" ({len(atualizados)} registro(s))."
            ),
            dados_depois={"processo_key": processo_key, "status_destino": status_destino, "processos_ids": atualizados},
        )
        return {
            "op_id": op_id,
            "processo_key": processo_key,
            "status_destino": status_destino,
            "processos_atualizados": atualizados,
        }

    def mover_kanban_proximo(self, op_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")

        processos = self._repository.list_processos(op_id, include_inactive=False)
        macro = self._macro_from_processos(processos)
        origem_key = self._text(payload.get("processo_origem")) or str(macro["processo_macro_key"])
        origem_key = origem_key.strip().lower()
        if origem_key not in PROCESSOS_CANONICOS:
            raise ValueError("processo_origem invalido")

        origem_ordem = int(PROCESSOS_CANONICOS[origem_key]["ordem"])
        destino_item = next((item for item in PROCESSOS_PADRAO if int(item["ordem"]) == origem_ordem + 1), None)
        if not destino_item:
            raise ValueError("processo atual ja esta na ultima etapa")
        destino_key = str(destino_item["processo_key"])

        status_destino = self._normalize_status_kanban(payload.get("status_destino") or "NAO_INICIADO")
        if status_destino not in STATUS_KANBAN_VALIDOS:
            raise ValueError("status_destino invalido para Kanban")

        op_produto_id = payload.get("op_produto_id")
        op_produto_id = int(op_produto_id) if op_produto_id not in (None, "") else None
        observacao = self._text(payload.get("observacao"))

        rows_all = macro["rows_all"]
        origem_rows = [
            row
            for row in rows_all
            if str(row.get("_processo_key")) == origem_key
            and (op_produto_id is None or int(row.get("op_produto_id") or 0) == op_produto_id)
        ]
        if not origem_rows:
            raise ValueError("nao ha itens da OP no processo de origem informado")

        produtos_move = {int(row.get("op_produto_id") or 0) for row in origem_rows}
        destino_rows = [
            row
            for row in rows_all
            if str(row.get("_processo_key")) == destino_key
            and int(row.get("op_produto_id") or 0) in produtos_move
        ]
        if not destino_rows:
            raise ValueError("processo de destino nao encontrado para os itens selecionados")

        origem_ids: List[int] = []
        destino_ids: List[int] = []
        for row in origem_rows:
            updated = self._apply_status_to_processo(op_id, row, "CONCLUIDO", observacao)
            origem_ids.append(int(updated.get("id") or 0))
        for row in destino_rows:
            updated = self._apply_status_to_processo(op_id, row, status_destino, observacao)
            destino_ids.append(int(updated.get("id") or 0))

        self.registrar_historico(
            op_id=op_id,
            entidade="OP_PROCESSO",
            entidade_id=None,
            acao="KANBAN_MOVIDO_PROCESSO",
            detalhe=(
                f"Kanban: mover do processo {origem_key} para {destino_key}"
                f" ({len(destino_ids)} item(ns))."
            ),
            dados_depois={
                "processo_origem": origem_key,
                "processo_destino": destino_key,
                "status_destino": status_destino,
                "origem_ids": origem_ids,
                "destino_ids": destino_ids,
            },
        )
        return {
            "op_id": op_id,
            "processo_origem": origem_key,
            "processo_destino": destino_key,
            "status_destino": status_destino,
            "processos_origem_finalizados": origem_ids,
            "processos_destino_atualizados": destino_ids,
        }

    def pular_kanban_processo(self, op_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")

        processos = self._repository.list_processos(op_id, include_inactive=False)
        macro = self._macro_from_processos(processos)
        origem_key = self._text(payload.get("processo_origem")) or str(macro["processo_macro_key"])
        destino_key = self._text(payload.get("processo_destino"))
        if not destino_key:
            raise ValueError("processo_destino obrigatorio")
        origem_key = origem_key.strip().lower()
        destino_key = destino_key.strip().lower()
        if origem_key not in PROCESSOS_CANONICOS or destino_key not in PROCESSOS_CANONICOS:
            raise ValueError("processo_origem/processo_destino invalido")
        if origem_key == destino_key:
            raise ValueError("processo_destino deve ser diferente do processo_origem")

        status_destino = self._normalize_status_kanban(payload.get("status_destino") or "NAO_INICIADO")
        if status_destino not in STATUS_KANBAN_VALIDOS:
            raise ValueError("status_destino invalido para Kanban")

        op_produto_id = payload.get("op_produto_id")
        op_produto_id = int(op_produto_id) if op_produto_id not in (None, "") else None
        observacao = self._text(payload.get("observacao"))

        rows_all = macro["rows_all"]
        origem_rows = [
            row
            for row in rows_all
            if str(row.get("_processo_key")) == origem_key
            and (op_produto_id is None or int(row.get("op_produto_id") or 0) == op_produto_id)
        ]
        if not origem_rows:
            raise ValueError("nao ha itens no processo de origem informado")

        produtos_move = {int(row.get("op_produto_id") or 0) for row in origem_rows}
        destino_rows = [
            row
            for row in rows_all
            if str(row.get("_processo_key")) == destino_key
            and int(row.get("op_produto_id") or 0) in produtos_move
        ]
        if not destino_rows:
            raise ValueError("nao ha processos de destino para os itens selecionados")

        origem_ids: List[int] = []
        destino_ids: List[int] = []
        for row in origem_rows:
            updated = self._apply_status_to_processo(op_id, row, "CONCLUIDO", observacao)
            origem_ids.append(int(updated.get("id") or 0))
        for row in destino_rows:
            updated = self._apply_status_to_processo(op_id, row, status_destino, observacao)
            destino_ids.append(int(updated.get("id") or 0))

        self.registrar_historico(
            op_id=op_id,
            entidade="OP_PROCESSO",
            entidade_id=None,
            acao="KANBAN_PULOU_PROCESSO",
            detalhe=f"Kanban: pulo de {origem_key} para {destino_key}.",
            dados_depois={
                "processo_origem": origem_key,
                "processo_destino": destino_key,
                "status_destino": status_destino,
                "origem_ids": origem_ids,
                "destino_ids": destino_ids,
            },
        )
        return {
            "op_id": op_id,
            "processo_origem": origem_key,
            "processo_destino": destino_key,
            "status_destino": status_destino,
            "processos_origem_finalizados": origem_ids,
            "processos_destino_atualizados": destino_ids,
        }

    def update_processo(self, op_id: int, processo_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        current = self._repository.get_processo(op_id, processo_id)
        if not current:
            raise ValueError("processo inexistente")

        updates: Dict[str, Any] = {}
        if "quantidade_concluida" in payload and payload.get("quantidade_concluida") is not None:
            qtd = self._float(payload.get("quantidade_concluida"), -1)
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
            op_id=op_id,
            entidade="OP_PROCESSO",
            entidade_id=processo_id,
            acao="PROCESSO_ATUALIZADO",
            detalhe=f"Processo {updated.get('processo_nome')} atualizado.",
            dados_antes=current,
            dados_depois=updated,
        )
        return updated

    def list_historico(self, op_id: int) -> List[Dict[str, Any]]:
        if not self._repository.get_ordem(op_id, include_inactive=False):
            raise ValueError("ordem de producao inexistente")
        return self._repository.list_historico(op_id)
