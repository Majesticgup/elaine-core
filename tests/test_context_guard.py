from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.elaine_context_guard import process


class ContextGuardTests(unittest.TestCase):
    def test_json_preserves_error_and_is_retrievable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "rows.json"
            rows = [{"id": i, "status": "ok", "message": "routine repeated value"} for i in range(100)]
            rows[67] = {"id": 67, "status": "FATAL", "message": "critical error"}
            source.write_text(json.dumps(rows), encoding="utf-8")

            output, receipt = process(source, "compress", root / "cache", 15, 40, 100)

            self.assertIn("critical error", output)
            json.loads(output)
            self.assertLess(receipt["bytes_after"], receipt["bytes_before"])
            self.assertIsNotNone(receipt["retrieval_ref"])
            self.assertEqual(
                Path(str(receipt["retrieval_ref"])).read_text(encoding="utf-8"),
                source.read_text(encoding="utf-8"),
            )

    def test_code_passthrough(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "example.py"
            source.write_text("print('x')\n" * 500, encoding="utf-8")

            output, receipt = process(source, "compress", root / "cache", 15, 40, 100)

            self.assertEqual(output, source.read_bytes().decode("utf-8"))
            self.assertEqual(receipt["strategy"], "passthrough-code")

    def test_short_passthrough(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "small.txt"
            source.write_text("small result\n", encoding="utf-8")

            output, receipt = process(source, "compress", root / "cache", 15, 40, 1200)

            self.assertEqual(output, source.read_bytes().decode("utf-8"))
            self.assertEqual(receipt["strategy"], "passthrough-short")


if __name__ == "__main__":
    unittest.main()
