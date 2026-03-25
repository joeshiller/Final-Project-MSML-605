import csv
from pathlib import Path
from datetime import datetime

import numpy as np
from loguru import logger

from msml605.metrics import apply_threshold, evaluate_predictions
from msml605.tracking import log_run, get_git_commit_hash


def load_scores_csv(path):
    scores = []
    labels = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scores.append(float(row["score"]))
            labels.append(int(row["label"]))

    return np.array(scores, dtype=float), np.array(labels, dtype=int)


def write_sweep_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "threshold",
                "accuracy",
                "balanced_accuracy",
                "tp",
                "tn",
                "fp",
                "fn",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    logger.info("Starting threshold sweep")

    input_path = Path("output-data/val_scores.csv")
    output_path = Path("output-data/threshold_sweep_val.csv")

    scores, labels = load_scores_csv(input_path)

    thresholds = np.linspace(scores.min(), scores.max(), 200)

    best_threshold = None
    best_metrics = None
    best_balanced_accuracy = -1.0
    sweep_rows = []

    for threshold in thresholds:
        preds = apply_threshold(scores, threshold)
        metrics = evaluate_predictions(labels, preds)

        row = {
            "threshold": float(threshold),
            "accuracy": metrics["accuracy"],
            "balanced_accuracy": metrics["balanced_accuracy"],
            "tp": metrics["tp"],
            "tn": metrics["tn"],
            "fp": metrics["fp"],
            "fn": metrics["fn"],
        }
        sweep_rows.append(row)

        if metrics["balanced_accuracy"] > best_balanced_accuracy:
            best_balanced_accuracy = metrics["balanced_accuracy"]
            best_threshold = float(threshold)
            best_metrics = metrics

    write_sweep_csv(output_path, sweep_rows)

    log_run(
        {
            "run_id": "run_001",
            "timestamp": datetime.utcnow().isoformat(),
            "commit_hash": get_git_commit_hash(),
            "config_name": "baseline",
            "data_version": "milestone1_pairs",
            "split": "val",
            "threshold_rule": "max_balanced_accuracy",
            "threshold_value": best_threshold,
            "accuracy": best_metrics["accuracy"],
            "balanced_accuracy": best_metrics["balanced_accuracy"],
            "tp": best_metrics["tp"],
            "tn": best_metrics["tn"],
            "fp": best_metrics["fp"],
            "fn": best_metrics["fn"],
            "note": "baseline validation threshold sweep",
        }
    )

    logger.info(f"Saved sweep results to {output_path}")
    logger.info(f"Best threshold: {best_threshold}")
    logger.info(f"Best balanced accuracy: {best_balanced_accuracy}")


if __name__ == "__main__":
    main()