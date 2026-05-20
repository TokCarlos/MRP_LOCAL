from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[3]
    app_path = project_root / "01-mrp" / "back_end" / "app"
    sys.path.insert(0, str(app_path))

    from adapters.produtos_seed_adapter import ProdutosSeedAdapter
    from repositories.produtos_repository import ProdutosRepository
    from services.produtos_service import ProdutosService

    adapter = ProdutosSeedAdapter(project_root=project_root)
    repo = ProdutosRepository(adapter=adapter)
    service = ProdutosService(repository=repo, project_root=project_root)
    report = service.validate()

    print("=== DIAGNOSTICO BACKEND PRODUTOS (SEED) ===")
    print(f"total_produtos: {report.total_produtos}")
    print(f"empresas_encontradas: {len(report.empresas)}")
    print(f"atas_encontradas: {len(report.atas)}")
    print(f"categorias_encontradas: {len(report.categorias)}")
    print(f"produtos_sem_imagem: {len(report.produtos_sem_imagem)}")
    print(f"imagens_inexistentes: {len(report.imagens_inexistentes)}")
    print(f"duplicidades_produto_key: {len(report.duplicidades_produto_key)}")
    print(f"duplicidades_item_empresa_ata: {len(report.duplicidades_item_empresa_ata)}")
    print(f"alertas: {len(report.alertas)}")
    print(f"erros: {len(report.erros)}")

    if report.imagens_inexistentes:
        print("\n[imagens_inexistentes]")
        for path in report.imagens_inexistentes[:20]:
            print(f"- {path}")

    if report.duplicidades_produto_key:
        print("\n[duplicidades_produto_key]")
        for key in report.duplicidades_produto_key:
            print(f"- {key}")

    if report.alertas:
        print("\n[alertas]")
        for alerta in report.alertas[:30]:
            print(f"- {alerta}")

    if report.erros:
        print("\n[erros]")
        for erro in report.erros:
            print(f"- {erro}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
