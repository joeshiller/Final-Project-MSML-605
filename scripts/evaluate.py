import argparse
import csv
import json
from pathlib import Path

import numpy as np
from loguru import logger

from msml605 import config, run
from msml605.metrics import apply_threshold, evaluate_predictions


def load_scores_csv(path):
    scores = []
    labels = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scores.append(float(row["score"]))
            labels.append(int(row["label"]))

    return np.array(scores, dtype=float), np.array(labels, dtype=int)


def write_eval_json(path, split, threshold, metrics):
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "split": split,
        "threshold": threshold,
        "accuracy": metrics["accuracy"],
        "balanced_accuracy": metrics["balanced_accuracy"],
        "tp": metrics["tp"],
        "tn": metrics["tn"],
        "fp": metrics["fp"],
        "fn": metrics["fn"],
    }

    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", required=True, choices=["val", "test"])
    parser.add_argument("--threshold", type=float, required=True)
    parser.add_argument("description")
    args = parser.parse_args()

    cfg = config.load_config(config.config_path)

    split = args.split
    threshold = args.threshold

    input_path = Path(cfg.output_dir) / f"{split}_scores.csv"
    output_path = Path(cfg.output_dir) / f"eval_{split}.json"

    logger.info(f"Starting fixed-threshold evaluation for {split}")

    scores, labels = load_scores_csv(input_path)
    preds = apply_threshold(scores, threshold)
    metrics = evaluate_predictions(labels, preds)

    write_eval_json(output_path, split, threshold, metrics)

    this_run = run.create_run(
        cfg,
        run.RunConfig(
            split=split,
            threshold_rule="fixed_selected_threshold",
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
        args.description,
    )

    run_path = run.write_run(this_run, cfg.get_run_dir())

    logger.info(f"Saved evaluation summary to {output_path}")
    logger.info(f"Wrote run to {run_path}")
    logger.info(
        f"tp={metrics['tp']}, tn={metrics['tn']}, fp={metrics['fp']}, fn={metrics['fn']}"
    )


if __name__ == "__main__":
    main()