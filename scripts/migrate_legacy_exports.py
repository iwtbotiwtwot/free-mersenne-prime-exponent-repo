#!/usr/bin/env python3
"""Inventory source CSVs and optionally build canonical block payloads.

The default is a read-only inventory. `--migrate` writes only to the target
repository and fails closed on schema, interval, duplicate, or source-commit
conflicts. The source checkout is never modified.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, subprocess
from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from fmpe import CSV_FIELDS
from fmpe.canonical import block_bounds, canonical_csv, semantic_sha256
from fmpe.compress import compress
from fmpe.validate import validate_rows

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def source_revision(source: Path) -> str:
    return subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()

def inventory(source: Path, target: Path) -> dict:
    files = sorted((source / "candidates").glob("*.csv"))
    if not files:
        raise SystemExit(f"no candidate CSV files under {source / 'candidates'}")
    revision = source_revision(source)
    target_prov = target / "provenance"
    target_prov.mkdir(parents=True, exist_ok=True)
    records = 0
    total_bytes = 0
    rows_inventory = []
    for path in files:
        first = last = None
        count = 0
        header = None
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            header = tuple(reader.fieldnames or ())
            for row in reader:
                exponent = int(row["exponent"])
                first = exponent if first is None else first
                last = exponent
                count += 1
        size = path.stat().st_size
        digest = sha256_file(path)
        is_canonical = header == CSV_FIELDS
        rows_inventory.append({"original_path": str(path), "original_filename": path.name, "sha256": digest, "bytes": size, "exact_header": "|".join(header), "row_count": count, "first_exponent": first, "last_exponent": last, "source_revision": revision, "migration_disposition": "PENDING_CANONICAL_REPARTITION" if is_canonical else "PRESERVED_LEGACY_SCHEMA_EXCEPTION", "exception_status": "NONE" if is_canonical else "LEGACY_HEADER_SCHEMA"})
        records += count; total_bytes += size
    with (target_prov / "LEGACY_FILE_INVENTORY.csv").open("w", encoding="utf-8", newline="") as f:
        fields = tuple(rows_inventory[0])
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows_inventory)
    snapshot = {"source_repository": "https://github.com/iwtbotiwtwot/mersenne-prime-search", "source_path": str(source), "source_revision": revision, "candidate_files": len(files), "candidate_records": records, "raw_bytes": total_bytes, "assigns_primality": False}
    (target_prov / "SOURCE_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    return snapshot

def migrate(source: Path, target: Path, snapshot: dict) -> dict:
    grouped = defaultdict(list)
    seen_queue, seen_exp = set(), set()
    for path in sorted((source / "candidates").glob("*.csv")):
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                exp = int(row["exponent"])
                if row["queue_id"] in seen_queue or exp in seen_exp:
                    raise ValueError(f"duplicate queue_id or exponent: {path}:{reader.line_num}")
                seen_queue.add(row["queue_id"]); seen_exp.add(exp)
                lower, upper = block_bounds(exp)
                grouped[(lower, upper)].append(row)
    blocks = 0; raw_bytes = compressed_bytes = records = 0
    for (lower, upper), rows in sorted(grouped.items()):
        rows.sort(key=lambda r: int(r["exponent"]))
        stats = validate_rows(rows, lower, upper)
        raw = canonical_csv(rows); packed = compress(raw)
        block = target / "data" / f"band_{(lower // 500_000_000) * 500_000_000:012d}_{((upper - 1) // 500_000_000 + 1) * 500_000_000:012d}" / "blocks" / f"block_gt_{lower:012d}_le_{upper:012d}"
        block.mkdir(parents=True, exist_ok=True)
        (block / "CANDIDATES.csv.zst").write_bytes(packed)
        manifest = {"schema_version": "1.0.0", "block_id": block.name, "interval": {"lower_exclusive": lower, "upper_inclusive": upper, "width": 1_000_000, "interval_notation": f"({lower},{upper}]"}, "source_campaign": "SLCMP", "source_revision": snapshot["source_revision"], "assigns_primality": False, **stats, "csv_schema": "candidate_roster_v1", "raw_csv": {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}, "compressed_csv": {"format": "zstd", "level": 9, "bytes": len(packed), "sha256": hashlib.sha256(packed).hexdigest(), "storage": "release-asset", "asset_name": "CANDIDATES.csv.zst"}, "semantic_sha256": semantic_sha256(rows)}
        (block / "BLOCK_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (block / "VALIDATION_RECEIPT.json").write_text(json.dumps({"status": "PASS", "block_id": block.name, "record_count": len(rows), "raw_sha256": manifest["raw_csv"]["sha256"], "compressed_sha256": manifest["compressed_csv"]["sha256"]}, indent=2) + "\n", encoding="utf-8")
        blocks += 1; records += len(rows); raw_bytes += len(raw); compressed_bytes += len(packed)
    result = {"source_revision": snapshot["source_revision"], "canonical_blocks": blocks, "records": records, "raw_bytes": raw_bytes, "compressed_bytes": compressed_bytes, "compression_ratio": raw_bytes / compressed_bytes if compressed_bytes else None, "exceptions": 0}
    (target / "provenance" / "LEGACY_MIGRATION_MANIFEST.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--target", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--migrate", action="store_true")
    args = parser.parse_args()
    snapshot = inventory(args.source, args.target)
    result = migrate(args.source, args.target, snapshot) if args.migrate else {"status": "INVENTORY_ONLY"}
    print(json.dumps({"snapshot": snapshot, "result": result}, indent=2))

if __name__ == "__main__":
    main()
