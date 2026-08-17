# Ingestion protocol

The migration command first inventories every source file and records a
SHA-256, exact header, byte size and row bounds. Canonical eighteen-field files
are repartitioned into `(lower, upper]` one-million blocks. A source with a
different header is preserved as an explicit exception and cannot be silently
coerced. Five-block production ingestion is atomic and writes through a
temporary staging area before any publication move.
