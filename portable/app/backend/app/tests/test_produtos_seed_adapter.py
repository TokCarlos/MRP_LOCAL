from pathlib import Path
import unittest

from adapters.produtos_seed_adapter import ProdutosSeedAdapter


class TestProdutosSeedAdapter(unittest.TestCase):
    def test_load_produtos_lista(self) -> None:
        root = Path(__file__).resolve().parents[5]
        adapter = ProdutosSeedAdapter(project_root=root)
        produtos = adapter.load_produtos()
        self.assertIsInstance(produtos, list)
        self.assertGreater(len(produtos), 0)
        self.assertIsInstance(produtos[0], dict)


if __name__ == "__main__":
    unittest.main()
