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

## Run `benchmark`
Show that Numpy is faster than Python.
```sh
uv run scripts/benchmark.py
```

## Run `score_pairs`
Compute Euclidean-distance scores for each validation pair.
```sh
uv run scripts/score_pairs.py
```

## Run `thresholds`
Run a threshold sweep.
```sh
uv run scripts/thresholds.py "Some description of the run"
```



## Milestone 2 Baseline
- reusing the deterministic Milestone 1 split and pair-generation policy with seed `123`
- Validation split is used for threshold selection
- Smaller values indicate pairs that are more likely to be the same identity

Baseline configuration:

```json
{
  "seed": 123,
  "input_dir": "input-data",
  "output_dir": "output-data",
  "pair_policy": {
    "train": { "num_pos": 1000, "num_neg": 1000 },
    "val": { "num_pos": 200, "num_neg": 200 },
    "test": { "num_pos": 200, "num_neg": 200 }
  }
}
```
## Threshold
- Choose the threshold on validation that maximizes balanced accuracy, to reduce bias to a single class
- We choose the threshold using the validation set only.  
- Our score is distance-based, so smaller scores mean two images are more likely to be the same person. 
- If the score is less than or equal to the threshold, we predict same person. Otherwise, we predict different people.
- After choosing the threshold on validation, we keep it fixed and use it on the test set.
- The best validation threshold for the baseline system was 20.56.
- After the data-centric improvement, the best validation threshold was `18.88`.
- We changed pair generation by adding a deterministic cap on positive candidate pairs per identity.

