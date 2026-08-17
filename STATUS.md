# Status

`INITIAL_CUSTODY_SCAFFOLD`: architecture, exact source inventory and validators
are installed. The source contains 54,385,839 records across 4,484 files at
revision `9df4957c458b68b4363938766052bc2ebb6c5db9`. One 1,858-row SLCMP0
legacy-schema exception is preserved in the ledger; complete migration remains
open until that file has a separate lossless legacy asset and receipt.

`ON_DEMAND_SOURCE_BAND_DOWNLOAD`: installed. `scripts/download_bands.py` lets
users choose live ordinary CSV data by exponent, interval or SLCMP run without
cloning the source repository. Each invocation pins one source revision,
validates downloaded rows and emits a SHA-256 receipt. This capability is
independent of the still-open compressed canonical-payload migration.
