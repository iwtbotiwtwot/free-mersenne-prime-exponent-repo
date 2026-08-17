"""Canonical interval, CSV and semantic-hash helpers."""
from __future__ import annotations
import csv, hashlib, io, json
from pathlib import Path
from . import CSV_FIELDS

def block_bounds(exponent: int) -> tuple[int, int]:
    upper = ((exponent // 1_000_000) + 1) * 1_000_000
    return upper - 1_000_000, upper

def block_id(lower: int, upper: int) -> str:
    return f"block_gt_{lower:012d}_le_{upper:012d}"

def canonical_csv(rows: list[dict[str, str]]) -> bytes:
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=CSV_FIELDS, lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: row.get(k, "") for k in CSV_FIELDS})
    return out.getvalue().encode("utf-8")

def semantic_sha256(rows: list[dict[str, str]]) -> str:
    h = hashlib.sha256()
    for row in rows:
        h.update(json.dumps([row.get(k, "") for k in CSV_FIELDS], ensure_ascii=False, separators=(",", ":")).encode())
        h.update(b"\n")
    return h.hexdigest()

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != CSV_FIELDS:
            raise ValueError(f"{path}: header does not match candidate_roster_v1")
        return list(reader)
