#!/usr/bin/env python3
"""Route a query to a canonical block without scanning the archive."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from fmpe.canonical import block_bounds, block_id

root = Path(__file__).parents[1]
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--exponent", type=int)
group.add_argument("--queue-id")
parser.add_argument("--range", nargs=2, type=int)
args = parser.parse_args()
if args.exponent is not None:
    lower, upper = block_bounds(args.exponent)
    print(json.dumps({"block_id": block_id(lower, upper), "interval": f"({lower},{upper}]", "exponent": args.exponent, "status": "ROUTED"}, indent=2))
else:
    print(json.dumps({"queue_id": args.queue_id, "status": "QUERY_REQUIRES_BLOCK_INDEX"}, indent=2))
