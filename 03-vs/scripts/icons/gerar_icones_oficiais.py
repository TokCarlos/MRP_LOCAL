from __future__ import annotations

import sys
from pathlib import Path

SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    source_dir = project_root / "01-mrp" / "assets" / "icons" / "source"
    out_dir = project_root / "01-mrp" / "assets" / "icons" / "windows" / "ico"
    preview_dir = project_root / "01-mrp" / "assets" / "icons" / "windows" / "preview"

    mapping = {
        "mrp_pcp_light.png": "mrp_pcp_light.ico",
        "mrp_jpl_dark.png": "mrp_jpl_dark.ico",
        "mrp_mrp_light.png": "mrp_mrp_light.ico",
        "mrp_mrp_dark.png": "mrp_mrp_dark.ico",
    }

    missing = [name for name in mapping if not (source_dir / name).exists()]
    if missing:
        print("ERRO: imagens fonte ausentes:")
        for name in missing:
            print(f"- {source_dir / name}")
        return 1

    try:
        from PIL import Image
    except Exception:
        print("ERRO: Pillow nao disponivel no ambiente. Nao foi possivel gerar ICO multi-resolucao.")
        print("Acao: instalar Pillow manualmente em etapa autorizada, ou gerar ICO por ferramenta externa.")
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)

    for png_name, ico_name in mapping.items():
        src = source_dir / png_name
        dst = out_dir / ico_name
        with Image.open(src) as image:
            rgba = image.convert("RGBA")
            rgba.save(dst, format="ICO", sizes=SIZES)
            preview_out = preview_dir / png_name
            rgba.save(preview_out, format="PNG")
        print(f"OK: {dst}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
