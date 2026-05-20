from __future__ import annotations

import struct
from pathlib import Path


REQUIRED = [
    "mrp_pcp_light.ico",
    "mrp_jpl_dark.ico",
    "mrp_mrp_light.ico",
    "mrp_mrp_dark.ico",
]


def read_ico_sizes(path: Path) -> list[tuple[int, int]]:
    data = path.read_bytes()
    if len(data) < 6:
        raise ValueError("ICO muito curto")
    reserved, icon_type, count = struct.unpack_from("<HHH", data, 0)
    if reserved != 0 or icon_type != 1 or count < 1:
        raise ValueError("Cabecalho ICO invalido")
    sizes: list[tuple[int, int]] = []
    for i in range(count):
        off = 6 + i * 16
        if off + 16 > len(data):
            raise ValueError("Entrada ICO truncada")
        w = data[off]
        h = data[off + 1]
        width = 256 if w == 0 else w
        height = 256 if h == 0 else h
        sizes.append((width, height))
    return sorted(set(sizes))


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    source = root / "01-mrp" / "assets" / "icons" / "source"
    ico_dir = root / "01-mrp" / "assets" / "icons" / "windows" / "ico"
    shortcut_script = root / "03-vs" / "scripts" / "painel" / "criar_atalho_painel.ps1"
    diag_script = root / "03-vs" / "scripts" / "painel" / "diagnosticar_atalho_painel.ps1"

    print("=== DIAGNOSTICO ICONES OFICIAIS ===")
    missing_source = []
    for png in ["mrp_pcp_light.png", "mrp_jpl_dark.png", "mrp_mrp_light.png", "mrp_mrp_dark.png"]:
        p = source / png
        if not p.exists():
            missing_source.append(str(p))
    if missing_source:
        print("ERRO: fontes PNG ausentes:")
        for item in missing_source:
            print(f"- {item}")
        return 1

    required_sizes = {(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)}
    errors = 0
    for name in REQUIRED:
        p = ico_dir / name
        if not p.exists():
            print(f"ERRO: ico ausente: {p}")
            errors += 1
            continue
        try:
            sizes = set(read_ico_sizes(p))
            print(f"OK: {name} sizes={sorted(sizes)}")
            missing_sizes = required_sizes - sizes
            if missing_sizes:
                print(f"ALERTA: {name} sem alguns tamanhos esperados: {sorted(missing_sizes)}")
        except Exception as exc:
            print(f"ERRO: {name} invalido ({exc})")
            errors += 1

    text = shortcut_script.read_text(encoding="utf-8")
    uses_localappdata = "LOCALAPPDATA" in text
    print(f"atalho_usa_localappdata: {uses_localappdata}")

    diag_text = diag_script.read_text(encoding="utf-8") if diag_script.exists() else ""
    print(f"diagnostico_atalho_existe: {diag_script.exists()}")
    print(f"diagnostico_sem_dll_padrao: {'MRP_ICONS.dll' not in diag_text}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
