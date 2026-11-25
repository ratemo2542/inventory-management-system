import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import main

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_db = main.DB
        main.DB = Path(self.tmp.name) / "inventory.db"

    def tearDown(self):
        main.DB = self.old_db
        self.tmp.cleanup()

    def run_cli(self, *args):
        with patch("sys.argv", ["main.py", *args]), contextlib.redirect_stdout(io.StringIO()) as output:
            main.main()
        return output.getvalue()

    def test_add_stock_and_low_stock_warning(self):
        self.run_cli("add", "--sku", "KB1", "--name", "Keyboard", "--price", "10", "--quantity", "2", "--reorder-level", "3")
        result = self.run_cli("list")
        self.assertIn("LOW STOCK", result)
        self.run_cli("stock", "KB1", "--change", "4")
        self.assertIn("qty=6", self.run_cli("list"))

if __name__ == "__main__":
    unittest.main()
