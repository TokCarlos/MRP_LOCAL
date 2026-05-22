from __future__ import annotations

from pathlib import Path


def normalize_rel_path(value: str) -> Path:
    normalized = value.replace("\\", "/")
    return Path(*[part for part in normalized.split("/") if part])

