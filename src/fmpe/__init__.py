"""Canonical data contracts for the free Mersenne exponent archive."""

SCHEMA_VERSION = "1.0.0"
CSV_FIELDS = (
    "queue_id", "queue_rank", "shell_survivor_rank", "exponent",
    "mersenne_object", "screen_status", "shell_status",
    "screen_schedule_count", "shell_schedule_count",
    "shell_tested_opportunity_count", "external_status_at_snapshot",
    "assignment_snapshot_utc", "sam_distribution_status", "assignee",
    "assignment_utc", "result_status", "result_reference", "notes",
)
