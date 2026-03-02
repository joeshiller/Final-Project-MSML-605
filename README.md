# Final-Project-MSML-605
## Overview
This repository ingests and processes the LFW dataset.

## Project Structure
- `src/` - Where the main logic lives.
- `scripts` - Where higher-level scripts that call into `src/` go.
- `input-data/` - Where downloaded data is stored.
- `output-data/` - Where outputed data goes.
- `configs/` - Where configuration files go.
- `tests/` - Where unit and integration tests go.

## Prerequisites
- `uv` - [uv github](https://github.com/astral-sh/uv)


# Commands


## Run `ingest_lfw`
Download and ingest the LFW dataset.
```sh
uv run scripts/ingest_lfw.py
```

## Run `make_pairs`
Split the dataset.
```sh
uv run scripts/make_pairs.py
```

## Run `similarity`
Show how similar these random pairs are.
```sh
uv run scripts/similarity.py
```

## Run `benchmark`
Show that Numpy is faster than Python.
```sh
uv run scripts/benchmark.py
```
