"""Independent validation primitives for candidate blocks."""
from __future__ import annotations
from . import CSV_FIELDS

COUNT_FIELDS = ("queue_rank", "shell_survivor_rank", "screen_schedule_count", "shell_schedule_count", "shell_tested_opportunity_count")

def validate_rows(rows, lower: int, upper: int) -> dict:
    queue_ids, exponents = set(), set()
    previous = None
    for index, row in enumerate(rows, 2):
        if tuple(row) != CSV_FIELDS:
            raise ValueError(f"row {index}: field order changed")
        exponent = int(row["exponent"])
        if not lower < exponent <= upper:
            raise ValueError(f"row {index}: exponent outside ({lower},{upper}]")
        if previous is not None and exponent <= previous:
            raise ValueError(f"row {index}: exponents are not strictly increasing")
        previous = exponent
        if exponent in exponents or row["queue_id"] in queue_ids:
            raise ValueError(f"row {index}: duplicate exponent or queue_id")
        exponents.add(exponent); queue_ids.add(row["queue_id"])
        if row["mersenne_object"] != f"2^{exponent}-1":
            raise ValueError(f"row {index}: mersenne_object disagrees with exponent")
        for field in COUNT_FIELDS:
            if row[field] and (not row[field].isdigit()):
                raise ValueError(f"row {index}: {field} is not a nonnegative integer")
    return {"record_count": len(rows), "first_exponent": min(exponents) if exponents else None, "last_exponent": max(exponents) if exponents else None, "duplicate_count": 0}
