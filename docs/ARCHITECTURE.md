# Architecture

Git stores schemas, manifests, indexes, validators and custody. Deterministic
Zstandard payloads carry complete rows. The manifest chain is global index to
band to five-block batch to one-million block to compressed CSV. The logical
schema already supports future release-asset storage through `storage`,
`repository` and `release` locators.
