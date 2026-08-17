#!/usr/bin/env python3
"""Metadata-only namespace simulation through 100 billion exponents."""
from __future__ import annotations
import json
from pathlib import Path
root = Path(__file__).parents[1]
bands = []
bands.append("band_000100000000_000500000000")
for lower in range(500_000_000, 100_000_000_000, 500_000_000):
    upper = lower + 500_000_000
    bands.append(f"band_{lower:012d}_{upper:012d}")
assert bands == sorted(bands) and len(bands) == len(set(bands))
result = {"status": "PASS", "bands": len(bands), "first": bands[0], "last": bands[-1], "max_exponent": 100_000_000_000, "materialized_rows": 0}
(root / "provenance/SCALE_SIMULATION_100B.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
