from __future__ import annotations

import re
import unicodedata


EMPRESA_NOME_BY_KEY = {"jpl": "JPL", "aco": "Aço", "tcr": "TCR"}


def ascii_key(value: str) -> str:
    txt = unicodedata.normalize("NFD", value or "")
    txt = "".join(ch for ch in txt if unicodedata.category(ch) != "Mn")
    txt = txt.lower()
    txt = re.sub(r"[^a-z0-9]+", "_", txt)
    return txt.strip("_")


def normalize_empresa_key(value: str) -> str:
    v = ascii_key(value)
    aliases = {"aco": "aco", "ao": "aco", "aço": "aco", "jpl": "jpl", "tcr": "tcr"}
    if v in aliases:
        return aliases[v]
    raise ValueError("empresa_invalida")


def normalize_ata_nome(value: str) -> str:
    src = (value or "").strip()
    key = ascii_key(src)
    if key in {"ata_sehis_gov_rj", "ata_gov_rio", "sehis_gov_rj", "sehis_gov_rio"}:
        return "SEHIS - GOV. RIO"
    return src


def normalize_ata_key(ata_nome: str, numero_ata: str) -> str:
    return f"{ascii_key(ata_nome)}__{ascii_key(numero_ata)}"


def build_produto_key(empresa_key: str, ata_key: str, item_ata: str) -> str:
    return f"{empresa_key}__{ata_key}__item_{ascii_key(item_ata)}"
