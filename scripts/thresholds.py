import argparse
import csv
from datetime import datetime
from pathlib import Path


import numpy as np
from loguru import logger

import msml605
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
    parser = argparse.ArgumentParser(
        prog="Threshold Sweep",
        description="yuh",
    )
    parser.add_argument("description")
    args = parser.parse_args()
    description = args.description

    cfg = config.load_config(config.config_path)

    logger.info("Starting threshold sweep")

    input_path = Path("output-data/val_scores.csv")
    output_path = Path("output-data/threshold_sweep_val.csv")

    scores, labels = load_scores_csv(input_path)

    # graph!
    import sklearn.metrics

    fpr, tpr, sk_threshold = sklearn.metrics.roc_curve(labels, -scores)
    roc_auc = sklearn.metrics.auc(fpr, tpr)
    import matplotlib.pyplot as plt

    plt.title("Receiver Operating Characteristic")
    plt.plot(fpr, tpr, "b", label="AUC = %0.2f" % roc_auc)
    plt.legend(loc="lower right")
    plt.plot([0, 1], [0, 1], "r--")
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.show()

    # done graphing

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
        logger.info(f"new row: {row}")

        if metrics["balanced_accuracy"] > best_balanced_accuracy:
            best_balanced_accuracy = metrics["balanced_accuracy"]
            best_threshold = float(threshold)
            best_metrics = metrics

    write_sweep_csv(output_path, sweep_rows)

    this_run = run.create_run(
        cfg,
        run.RunConfig(
            split="val",
            threshold_rule="max_balanced_accuracy",
            threshold_value=best_threshold,
        ),
        run.RunMetrics(
            accuracy=best_metrics["accuracy"],
            balanced_accuracy=best_metrics["balanced_accuracy"],
            true_positive=best_metrics["tp"],
            true_negative=best_metrics["tn"],
            false_positive=best_metrics["fp"],
            false_negative=best_metrics["fn"],
        ),
        description,
    )
    run_path = run.write_run(this_run, cfg.get_run_dir())
    logger.info(f"Wrote run to {run_path}")

    logger.info(f"Saved sweep results to {output_path}")
    logger.info(f"Best threshold: {best_threshold}")
    logger.info(f"Best balanced accuracy: {best_balanced_accuracy}")


if __name__ == "__main__":
    main()
