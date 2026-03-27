import json
from pathlib import Path

from msml605 import config, load_data, manifest, pairs, run
from msml605.metrics import apply_threshold, evaluate_predictions


def test_integrate():
    cfg = config.load_config("tests/config.json")

    # ingest data
    raw = load_data.load_dataset(cfg.input_dir)
    train, val, test = load_data.split_dataset(raw, cfg.output_dir)

    seed = cfg.seed
    man = manifest.DataManifest(
        seed=seed,
        split_policy="identity",
        counts=[
            [
                len(train),
                sum(train["images"]),
            ],
            [
                len(val),
                sum(val["images"]),
            ],
            [
                len(test),
                sum(test["images"]),
            ],
        ],
        data_source=manifest.DataSource(
            url="file://somewhere-lol", version="TEST", cache_dir=cfg.input_dir
        ),
    )

    manifest.write_manifest(man, f"{cfg.output_dir}/manifest.json")

    manifest_path = Path(cfg.output_dir) / "manifest.json"
    assert manifest_path.exists()

    # make_pairs
    summaries = []
    for split in ["train", "val", "test"]:
        summaries.append(
            pairs.generate_pairs_for_split(
                cfg.pair_policy, Path(cfg.output_dir), cfg.seed, split
            )
        )

    assert (Path(cfg.output_dir) / "pairs_train.csv").exists()
    assert (Path(cfg.output_dir) / "pairs_val.csv").exists()
    assert (Path(cfg.output_dir) / "pairs_test.csv").exists()

    # small evaluation path
    # scored validation examples
    scores = [10.0, 25.0, 30.0, 12.0]
    labels = [1, 0, 1, 0]
    threshold = 20.0

    preds = apply_threshold(scores, threshold)
    metrics = evaluate_predictions(labels, preds)

    assert metrics["tp"] == 1
    assert metrics["tn"] == 1
    assert metrics["fp"] == 1
    assert metrics["fn"] == 1
    assert metrics["accuracy"] == 0.5
    assert metrics["balanced_accuracy"] == 0.5

    # log a run 
    this_run = run.create_run(
        cfg,
        run.RunConfig(
            split="val",
            threshold_rule="max_balanced_accuracy",
            threshold_value=threshold,
        ),
        run.RunMetrics(
            accuracy=metrics["accuracy"],
            balanced_accuracy=metrics["balanced_accuracy"],
            true_positive=metrics["tp"],
            true_negative=metrics["tn"],
            false_positive=metrics["fp"],
            false_negative=metrics["fn"],
        ),
        "integration test run",
    )

    run_path = Path(run.write_run(this_run, cfg.get_run_dir()))
    assert run_path.exists()

    with open(run_path) as f:
        saved_run = json.load(f)
# Confirm taht it stored the expected threshold
    assert saved_run["threshold_info"]["split"] == "val"
    assert saved_run["threshold_info"]["threshold_rule"] == "max_balanced_accuracy"
    assert saved_run["threshold_info"]["threshold_value"] == threshold
# Confirm it stored the expected metrics
    assert saved_run["metrics"]["accuracy"] == 0.5
    assert saved_run["metrics"]["balanced_accuracy"] == 0.5
    assert saved_run["metrics"]["true_positive"] == 1
    assert saved_run["metrics"]["true_negative"] == 1
    assert saved_run["metrics"]["false_positive"] == 1
    assert saved_run["metrics"]["false_negative"] == 1