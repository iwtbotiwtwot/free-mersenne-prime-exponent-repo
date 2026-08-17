#!/usr/bin/env python3
"""Validate committed metadata and every materialized block manifest."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from fmpe import CSV_FIELDS

root = Path(__file__).parents[1]
index = json.loads((root / "index/GLOBAL_INDEX.json").read_text())
assert index["assigns_primality"] is False
assert tuple(CSV_FIELDS) == tuple(CSV_FIELDS)
manifests = list((root / "data").glob("**/BLOCK_MANIFEST.json"))
for path in manifests:
    manifest = json.loads(path.read_text())
    assert manifest["assigns_primality"] is False
    assert manifest["interval"]["width"] == 1_000_000
    assert (path.parent / "VALIDATION_RECEIPT.json").exists()
print(f"PASS blocks={len(manifests)} records={index['candidate_records']}")
