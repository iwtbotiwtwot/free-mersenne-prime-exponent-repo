# Getting started without Git expertise

## What is an exponent record?

A Mersenne number has the form `2^p - 1`. This repository records candidate
values of the exponent `p` after SAM/SLC structural and factor screening. Each
row keeps eighteen fields so the exponent, screening state, queue position and
any later assignment or result can travel together.

A row is a candidate record. A blank result field means no exact result has
been installed in that row.

## Easiest route: ordinary CSV files

If you want to browse or download regular CSV files one at a time, go to the
original [`mersenne-prime-search`](https://github.com/iwtbotiwtwot/mersenne-prime-search)
repository, open its `candidates` folder and choose an `SLCMP<number>.csv`
file. On the file page, use the download button to save it. CSV files can be
opened by LibreOffice Calc, Microsoft Excel, Numbers, a text editor, Python or
R.

## New archive route

This repository reorganizes the same complete records into exact
one-million-exponent blocks. Five neighboring blocks form one five-million
batch. Index files identify the interval, record count, SHA-256 checksum and
storage location for each payload.

Intervals use `lower < p <= upper`. For example, the block described as
`2,053,000,000 < p <= 2,054,000,000` excludes the lower endpoint and includes
the upper endpoint.

When migrated payloads are available:

1. Open `index/GLOBAL_INDEX.json`.
2. Find the band and batch containing your exponent.
3. Follow the block entry whose lower and upper bounds contain it.
4. Download the listed `.csv.zst` payload.
5. Decompress it with Zstandard, then open the resulting CSV.

On Linux, macOS or Windows with the `zstd` command installed:

```bash
zstd -d SLCMP4483.csv.zst
```

## Download selected live bands with Python

The installed downloader retrieves ordinary CSV bands directly from the live
source publication without cloning either repository. It first pins the exact
GitHub `main` revision, so a growing publication stream cannot change halfway
through one selection. It then validates every file and writes a SHA-256
download receipt.

Download the band containing one exponent:

```bash
python scripts/download_bands.py --exponent 2051000009
```

Download one named publication run:

```bash
python scripts/download_bands.py --run SLCMP4504
```

Download every source band overlapping a chosen interval:

```bash
python scripts/download_bands.py \
  --range 2050000000 2055000000 \
  --output my_bands
```

The interval selector means `(LOWER,UPPER]`. Repeat or combine `--run`,
`--exponent` and `--range` to make one exact selection. Add `--list-only` to
show what would be downloaded. Python 3 is the only software dependency.

## Download the project without Git

On the repository's main GitHub page, select `Code` and then `Download ZIP`.
Unzip the downloaded file normally. You only need a Git client if you want to
track updates as commits.

## Check a downloaded payload

Every installed payload has a SHA-256 checksum in its manifest. A checksum
confirms that the downloaded bytes match the published file.

```bash
sha256sum path/to/payload.csv.zst
```

Compare the printed value with the manifest's `sha256` field. Windows users
can use `certutil -hashfile path\to\payload.csv.zst SHA256`.

## Field meanings

See [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) for the eighteen columns. The
important distinction is between screening and primality: surviving the
installed screens leaves a candidate for later work; it does not fill in a
prime or composite result by itself.

## Current availability

Read [`STATUS.md`](../STATUS.md) first. The initial repository release installs
the archive design, exact source inventory, schemas and validators. Payload
migration is installed only when the status and indexes identify completed
payloads.
