# Free Mersenne Prime Exponent Repository

A free, machine-readable archive of Mersenne prime-exponent candidate records
carrying their complete SAM/SLC structural-screen, directional-shell,
scheduling, distribution and result information.

Candidate inclusion does not assign primality. A candidate with no exact result
remains unresolved; exact factor and Lucas--Lehmer authorities remain separate.

## Data contract

Records retain all eighteen source fields in [`candidate_roster_v1.json`](schemas/candidate_roster_v1.json).
Intervals use `lower < p <= upper`; see [`INTERVAL_CONVENTION.md`](docs/INTERVAL_CONVENTION.md).
Large immutable payloads are deterministic Zstandard files with SHA-256 hashes
and a manifest chain from [`index/GLOBAL_INDEX.json`](index/GLOBAL_INDEX.json)
through bands, batches and blocks.

## Verification and query

```bash
python scripts/validate_full.py
python scripts/query_exponent.py --exponent 2051000009
python scripts/query_exponent.py --queue-id SLCMP4483-000001
```

The source repository is [`mersenne-prime-search`](https://github.com/iwtbotiwtwot/mersenne-prime-search).
The exact imported source revision is recorded in `provenance/SOURCE_SNAPSHOT.json`.

## Attribution and license

Sean Brady is SAM/SLC originator, conceptual director, author and research
lead. OpenAI ChatGPT and Codex are AI research collaborators, technical
contributors and co-authors where applicable. Source code is Apache-2.0;
documentation is CC BY 4.0; generated artifacts are governed by their
manifests. See [`CITATION.cff`](CITATION.cff), [`LICENSE`](LICENSE) and
[`STEWARDSHIP_PLEDGE.md`](STEWARDSHIP_PLEDGE.md).
