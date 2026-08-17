#!/usr/bin/env python3
"""Download selected public Mersenne exponent bands at one pinned revision."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

REPOSITORY = "iwtbotiwtwot/mersenne-prime-search"
API_REF = f"https://api.github.com/repos/{REPOSITORY}/git/ref/heads/main"
RAW_ROOT = f"https://raw.githubusercontent.com/{REPOSITORY}"
ROW_PATTERN = re.compile(
    r"^\| \[(SLCMP[0-9]+)\]\(candidates/\1\.csv\) \| "
    r"`([0-9,]+) < p <= ([0-9,]+)` \| ([0-9,]+) \|$",
    re.MULTILINE,
)


def request_bytes(url: str) -> bytes:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "fmpe-band-downloader/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code} while reading {url}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"network error while reading {url}: {error.reason}") from error


def resolve_revision(requested: str | None) -> str:
    if requested:
        if not re.fullmatch(r"[0-9a-fA-F]{40}", requested):
            raise ValueError("--revision must be a full 40-character Git commit SHA")
        return requested.lower()
    value = json.loads(request_bytes(API_REF))
    revision = str(value["object"]["sha"])
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise RuntimeError("GitHub returned an invalid main revision")
    return revision


def parse_public_index(readme: str) -> list[dict[str, int | str]]:
    rows = [
        {
            "run_id": run_id,
            "lower_exclusive": int(lower.replace(",", "")),
            "upper_inclusive": int(upper.replace(",", "")),
            "candidate_count": int(count.replace(",", "")),
        }
        for run_id, lower, upper, count in ROW_PATTERN.findall(readme)
    ]
    if not rows:
        raise RuntimeError("no public candidate-band rows found in the pinned README")
    if len({row["run_id"] for row in rows}) != len(rows):
        raise RuntimeError("duplicate SLCMP run IDs in the pinned README")
    return rows


def choose_rows(index: list[dict[str, int | str]], runs: Iterable[str],
                exponents: Iterable[int], ranges: Iterable[tuple[int, int]]) -> list[dict[str, int | str]]:
    selected: dict[str, dict[str, int | str]] = {}
    by_run = {str(row["run_id"]).upper(): row for row in index}
    for requested in runs:
        run_id = requested.upper()
        if not run_id.startswith("SLCMP"):
            run_id = f"SLCMP{run_id}"
        if run_id not in by_run:
            raise ValueError(f"run is not present at the pinned revision: {run_id}")
        selected[run_id] = by_run[run_id]
    for exponent in exponents:
        matches = [row for row in index if int(row["lower_exclusive"]) < exponent <= int(row["upper_inclusive"])]
        if not matches:
            raise ValueError(f"no published band contains exponent {exponent}")
        if len(matches) != 1:
            raise RuntimeError(f"published intervals overlap at exponent {exponent}")
        selected[str(matches[0]["run_id"])] = matches[0]
    for lower, upper in ranges:
        if lower >= upper:
            raise ValueError(f"range must use LOWER < UPPER: {lower} {upper}")
        matches = [
            row for row in index
            if int(row["lower_exclusive"]) < upper and int(row["upper_inclusive"]) > lower
        ]
        if not matches:
            raise ValueError(f"no published bands overlap ({lower},{upper}]")
        for row in matches:
            selected[str(row["run_id"])] = row
    return sorted(selected.values(), key=lambda row: (int(row["lower_exclusive"]), str(row["run_id"])))


def validate_csv(data: bytes, row: dict[str, int | str]) -> dict[str, int | str | None]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RuntimeError(f"{row['run_id']}: CSV is not UTF-8") from error
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if not reader.fieldnames or "exponent" not in reader.fieldnames:
        raise RuntimeError(f"{row['run_id']}: CSV lacks an exponent column")
    lower, upper = int(row["lower_exclusive"]), int(row["upper_inclusive"])
    prior = None
    first = last = None
    count = 0
    for line_number, record in enumerate(reader, 2):
        try:
            exponent = int(record["exponent"])
        except (TypeError, ValueError) as error:
            raise RuntimeError(f"{row['run_id']}:{line_number}: invalid exponent") from error
        if not lower < exponent <= upper:
            raise RuntimeError(f"{row['run_id']}:{line_number}: exponent outside ({lower},{upper}]")
        if prior is not None and exponent <= prior:
            raise RuntimeError(f"{row['run_id']}:{line_number}: exponents are not strictly increasing")
        prior = exponent
        first = exponent if first is None else first
        last = exponent
        count += 1
    if count != int(row["candidate_count"]):
        raise RuntimeError(f"{row['run_id']}: expected {row['candidate_count']} rows, found {count}")
    return {"row_count": count, "first_exponent": first, "last_exponent": last,
            "header_fields": len(reader.fieldnames)}


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    selectors = parser.add_argument_group("selectors (use one or combine several)")
    selectors.add_argument("--run", action="append", default=[], help="SLCMP run ID, e.g. SLCMP4504")
    selectors.add_argument("--exponent", action="append", type=int, default=[], help="download the band containing P")
    selectors.add_argument("--range", action="append", nargs=2, type=int, metavar=("LOWER", "UPPER"), default=[],
                           help="download every band overlapping (LOWER,UPPER]")
    parser.add_argument("--output", type=Path, default=Path("downloaded_bands"))
    parser.add_argument("--revision", help="pin an explicit full source commit SHA")
    parser.add_argument("--list-only", action="store_true", help="show the selection without downloading CSVs")
    args = parser.parse_args()
    if not (args.run or args.exponent or args.range):
        parser.error("select at least one --run, --exponent, or --range")

    revision = resolve_revision(args.revision)
    readme_url = f"{RAW_ROOT}/{revision}/README.md"
    index = parse_public_index(request_bytes(readme_url).decode("utf-8"))
    selected = choose_rows(index, args.run, args.exponent, [tuple(value) for value in args.range])
    plan = {"repository": REPOSITORY, "revision": revision, "selected_bands": selected}
    if args.list_only:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return

    receipts = []
    for row in selected:
        run_id = str(row["run_id"])
        url = f"{RAW_ROOT}/{revision}/candidates/{run_id}.csv"
        data = request_bytes(url)
        validation = validate_csv(data, row)
        destination = args.output / f"{run_id}.csv"
        atomic_write(destination, data)
        receipts.append({**row, **validation, "path": str(destination), "bytes": len(data),
                         "sha256": hashlib.sha256(data).hexdigest(), "source_url": url,
                         "status": "PASS"})
        print(f"PASS {run_id} rows={validation['row_count']} path={destination}", file=sys.stderr)

    receipt = {
        "schema": "FMPE_SELECTED_BAND_DOWNLOAD_RECEIPT_V1",
        "status": "PASS",
        "repository": REPOSITORY,
        "revision": revision,
        "downloaded_utc": utc_now(),
        "assigns_primality": False,
        "files": receipts,
        "aggregate": {"bands": len(receipts), "candidate_records": sum(int(row["row_count"]) for row in receipts),
                      "bytes": sum(int(row["bytes"]) for row in receipts)},
    }
    receipt_path = args.output / "DOWNLOAD_RECEIPT.json"
    atomic_write(receipt_path, (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
