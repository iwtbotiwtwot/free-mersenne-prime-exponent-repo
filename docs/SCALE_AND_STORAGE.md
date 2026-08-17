# Scale and storage decision

The initial archive is designed for Git metadata plus public release assets
for large immutable payloads. This avoids Git LFS and preserves free,
machine-readable downloads. The first migration records exact raw and
compressed hashes before any asset publication. A 100-billion-exponent
namespace is metadata-only and does not allocate billions of row files.

GitHub's live limits must be rechecked at release time; this document does not
treat a remembered limit as a current verification receipt.
