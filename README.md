# Final-Project-MSML-605

## Project Structure
- `src/` - Where the main logic lives.
- `scripts` - Where higher-level scripts that call into `src/` go.
- `input-data/` - Where downloaded data is stored.
- `output-data/` - Where outputed data goes.
- `configs/` - Where configuration files go.
- `tests/` - Where unit and integration tests go.

## Prerequisites
- `uv`


# Commands

## Run `bench_similarity`
```sh
uv run scripts/bench_similarity.py
```

## Run `ingest_lfw`
```sh
uv run scripts/ingest_lfw.py
```

## Run `make_pairs`
```sh
uv run scripts/make_pairs.py
```
