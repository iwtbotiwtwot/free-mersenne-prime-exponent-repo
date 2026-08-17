from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).parents[1] / "scripts/download_bands.py"
SPEC = importlib.util.spec_from_file_location("download_bands", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DownloadBandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.readme = """\
| [SLCMP21](candidates/SLCMP21.csv) | `147,500,000 < p <= 147,750,000` | 2 |
| [SLCMP22](candidates/SLCMP22.csv) | `147,750,000 < p <= 148,000,000` | 1 |
| **Total** |  | **3** |
"""
        self.index = MODULE.parse_public_index(self.readme)

    def test_choose_by_exponent_and_run(self) -> None:
        selected = MODULE.choose_rows(self.index, ["22"], [147_700_003], [])
        self.assertEqual([row["run_id"] for row in selected], ["SLCMP21", "SLCMP22"])

    def test_choose_overlapping_range(self) -> None:
        selected = MODULE.choose_rows(self.index, [], [], [(147_749_999, 147_750_001)])
        self.assertEqual([row["run_id"] for row in selected], ["SLCMP21", "SLCMP22"])

    def test_validate_csv(self) -> None:
        data = b"queue_id,exponent,mersenne_object\nq1,147800003,2^147800003-1\n"
        result = MODULE.validate_csv(data, self.index[1])
        self.assertEqual(result["row_count"], 1)


if __name__ == "__main__":
    unittest.main()
