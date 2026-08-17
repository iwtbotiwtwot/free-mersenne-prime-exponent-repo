# Free Mersenne Prime Exponent Repository

This project is a free, machine-readable library of screened Mersenne exponent
candidates. In plain language: each record starts with a prime exponent `p`
for the number `2^p - 1`, then keeps the complete SAM/SLC screening,
scheduling, distribution and result information associated with that exponent.

You do not need to know Git or GitHub to use the data. Start with
[`GETTING_STARTED.md`](docs/GETTING_STARTED.md) for browser downloads,
spreadsheet use and simple command-line searches.

Candidate inclusion does not assign primality. A candidate with no exact result
remains unresolved; exact factor and Lucas--Lehmer authorities remain separate.

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

1. Click `Code`, then `Download ZIP`, to download the repository without Git.
2. Read [`STATUS.md`](STATUS.md) to see which payloads are currently available.
3. When payload migration is installed, use the index to locate the
   one-million interval containing your exponent.
4. Decompress that block and open the CSV in a spreadsheet, text editor or
   data-analysis program.

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
