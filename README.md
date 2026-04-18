# Final-Project-MSML-605
## Overview
This repository ingests and processes the LFW dataset.

## Project Structure
- `reports/` - Where reports are.
- `src/` - Where the main logic lives.
- `scripts` - Where higher-level scripts that call into `src/` go.
- `input-data/` - Where downloaded data is stored.
- `output-data/` - Where outputed data goes.
  - `data-source.json` - A description of the current data stored in `input-data/`. # TODO: should this go in input-data/ ?
  - `runs/` - Where all runs live.
    - `run_<run UUID>` - Basic information about the run.
      - `run_<run UUID>.json` - Description of the run.
      - `pairs_{test, train, val}.csv`
      - `test_identities.csv`
      - `test_scores.csv`
      - `threshold_sweep_val.csv`
      - `{test, train, val}_identities.csv`
      - `{test, train, val}_scores.csv`
- `configs/` - Where configuration files go.
  - `config.json` - The config the next run will copy.
  - `environment.json` - Configurations for where data is located in the project. Not copied.
- `tests/` - Where unit and integration tests go.

## Prerequisites
- `uv` - [uv github](https://github.com/astral-sh/uv)


# Commands


## Run `ingest_lfw`
Download and ingest the LFW dataset.
```sh
uv run scripts/ingest_lfw.py
```

## Create Run
```sh
uv run scripts/create_run.py "some description"
```
which will output the run ID.


## Run Preprocess
Split the dataset.
```sh
uv run scripts/preprocess.py --run <run id>
```

## Generate Embeddings
```sh
uv run scripts/generate_embeddings.py --run <run id>
```


## Run `score_pairs`
Compute Euclidean-distance scores for each validation pair.
```sh
uv run scripts/score_pairs.py --split=[train | val | test] --run <run id>
```

## Run `thresholds`
Run a threshold sweep.
```sh
uv run scripts/thresholds.py "Some description of the run"
```

## Calculate Confidence

## Load test

## Run `benchmark`
Show that Numpy is faster than Python.
```sh
uv run scripts/benchmark.py
```


## Run the tests
```sh
uv run pytest
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


The selected baseline is `20.5641134801839`. The run is located in `fixed-runs/` in with an id of `df035d4b-5818-4579-9bce-15cb879de875`.
Here's the confusion matrix for this run:
|    | Actually Positive | Actually Negative |
|---|---|---|
|Predicted Positive|98|68|
|Predicted Negative|102|132|


The selected post-change validation threshold is `18.87954639433729`. The run is located in `fixed-runs/` with an id of `f565dfef-4b9a-49ea-b2e9-b3932affb7e7`.

Here’s the confusion matrix for this run:
|    | Actually Positive | Actually Negative |
|---|---|---|
|Predicted Positive|80|43|
|Predicted Negative|120|157|
