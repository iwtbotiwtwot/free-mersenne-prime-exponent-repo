# Free Mersenne Prime Exponent Repository

This project is a free, machine-readable library of screened Mersenne exponent
candidates. In plain language: each record starts with a prime exponent `p`
for the number `2^p - 1`, then keeps the complete SAM/SLC screening,
scheduling, distribution and result information associated with that exponent.

**Current public search surface:** **179,384,892** primality-unassigned
candidate records published contiguously through **SLCMP8104**, ending at the
interval boundary **5,673,000,000**. The live total and ordinary CSV files are
maintained in the original
[`mersenne-prime-search`](https://github.com/iwtbotiwtwot/mersenne-prime-search)
repository.

You do not need to know Git or GitHub to use the data. Start with
[`GETTING_STARTED.md`](docs/GETTING_STARTED.md) for browser downloads,
spreadsheet use and simple command-line searches.

Candidate inclusion does not assign primality. A candidate with no exact result
remains unresolved; exact factor and Lucas--Lehmer authorities remain separate.

## This is a research idea, not just a large number

SAM begins from a different picture of prime search. A prime exponent is not
used only as a point on the uniform integer line; it is also treated as an
**informational radix mark** in a prime-only coordinate system. The exponent
history and the Mersenne recurrence supply two reciprocal information voices
on one closed geometry. Their nested rhythms—“beats within beats,” delayed
echoes and directional returns—identify structured places where exact factor
arithmetic should look.

That distinction is the heart of the project:

> Prime arithmetic is the certificate. Informational geometry decides where
> exact arithmetic should look.

SAM/SLC may schedule the work, but it does not get to declare the answer. An
exact divisor remains an ordinary modular-arithmetic certificate. A surviving
row remains unresolved until an exact primality test and the required result
custody close its status.

## Follow the ideas

- **Why primes become an informational ruler.** Read
  [SAM in Mersenne Search](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/main/SAM_IN_MERSENNE_SEARCH.md)
  for the clean-sheet line from prime-only coordinates and reciprocal orbits
  to structural factor work and the public candidate surface.
- **Why Mersenne closure has directional memory.** The reciprocal Lucas--Lehmer
  view isolates a signed preterminal amplitude before terminal closure. The
  common state can resolve and return while a separate directional ledger
  retains the route into that resolution: **state returns; history does not**.
  The broader computational setting is the public
  [Substrate Ledger Computer](https://github.com/iwtbotiwtwot/substrate-ledger-computer).
- **What SAM means by a write.** A write is not an anonymous scalar update. In
  the W8/X1/W9 algebra it is a typed activation, reciprocal relay, resolved
  receipt, local return and retained directional history. See the
  [Exact Write installation record](https://github.com/iwtbotiwtwot/SAM_Research_Project/blob/main/SAM_HISTORY/entries/H000132_2026-08-09_SLCV1_EXACT_WRITE_ALGEBRA_INSTALLATION.md)
  and the computation spine linked from the SAM repository.
- **Where reciprocal history leads analytically.** The RH program carries the
  same two-view history architecture into completed Weil forms, directional
  fibers, exact sign instruments and the current cutoff-wide contraction
  question. Read
  [RH Work to Date](https://github.com/iwtbotiwtwot/riemann-hypothesis-program/blob/main/RH_WORK_TO_DATE_V1_2026-08-15.md)
  or explore the full
  [Riemann Hypothesis Program](https://github.com/iwtbotiwtwot/riemann-hypothesis-program).

Together these links tell the larger story: the substrate record can compute;
reciprocal history can carry prime structure; prime structure can direct exact
work; and the resulting candidate surface can be tested independently by
anyone.

## Which repository should I use?

- Use this repository for the new free archive layout: compressed one-million
  blocks, five-million batches, indexes, hashes and validation tools.
- If you want the old-fashioned layout—one ordinary CSV file per historical
  SLCMP run—use the original
  [`mersenne-prime-search`](https://github.com/iwtbotiwtwot/mersenne-prime-search)
  repository. Its files can be opened or downloaded directly without using the
  new archive tools.

The original repository remains the source publication stream. This archive
imports those records without changing their eighteen fields.

## Data contract

Records retain all eighteen source fields in [`candidate_roster_v1.json`](schemas/candidate_roster_v1.json).
Intervals use `lower < p <= upper`; see [`INTERVAL_CONVENTION.md`](docs/INTERVAL_CONVENTION.md).
Large immutable payloads are deterministic Zstandard files with SHA-256 hashes
and a manifest chain from [`index/GLOBAL_INDEX.json`](index/GLOBAL_INDEX.json)
through bands, batches and blocks.

## Quick use

Python users can download only the live public bands they choose. The command
pins one exact source revision, validates interval and row-count custody, and
writes `DOWNLOAD_RECEIPT.json` with SHA-256 hashes:

```bash
python scripts/download_bands.py --exponent 2051000009
python scripts/download_bands.py --run SLCMP4504
python scripts/download_bands.py --range 2050000000 2055000000 --output my_bands
```

Use `--list-only` to inspect the selection without downloading CSV files.
Selectors may be combined and repeated. No third-party Python packages or Git
client are required.

For browser-only use, click `Code`, then `Download ZIP`, and follow
[`GETTING_STARTED.md`](docs/GETTING_STARTED.md). Read [`STATUS.md`](STATUS.md)
for the separate compressed-archive migration state.

For people comfortable with a terminal:

```bash
python scripts/validate_full.py
python scripts/query_exponent.py --exponent 2051000009
python scripts/query_exponent.py --queue-id SLCMP4483-000001
```

The validators and query commands operate on installed archive payloads. The
current initial release is a custody scaffold and exact source inventory; see
[`STATUS.md`](STATUS.md) before expecting migrated payload files.

The source and old-fashioned repository is
[`mersenne-prime-search`](https://github.com/iwtbotiwtwot/mersenne-prime-search).
The exact imported source revision is recorded in `provenance/SOURCE_SNAPSHOT.json`.

## Attribution and license

Sean Brady is SAM/SLC originator, conceptual director, author and research
lead. OpenAI ChatGPT and Codex are AI research collaborators, technical
contributors and co-authors where applicable. Source code is Apache-2.0;
documentation is CC BY 4.0; generated artifacts are governed by their
manifests. See [`CITATION.cff`](CITATION.cff), [`LICENSE`](LICENSE) and
[`STEWARDSHIP_PLEDGE.md`](STEWARDSHIP_PLEDGE.md).
