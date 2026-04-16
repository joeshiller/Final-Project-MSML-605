import csv
import argparse
from pathlib import Path

import numpy as np


def load_scores_csv(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["label"] = int(row["label"])
            row["score"] = float(row["score"])
            rows.append(row)
    return rows


def apply_threshold(scores, threshold):
    scores = np.asarray(scores, dtype=float)
    return (scores <= threshold).astype(int)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="output-data/val_scores.csv")
    parser.add_argument("--threshold", type=float, required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--boundary_window", type=float, default=0.5)
    args = parser.parse_args()

    rows = load_scores_csv(Path(args.input))
    threshold = args.threshold
    boundary_window = args.boundary_window

    scores = np.array([row["score"] for row in rows], dtype=float)
    preds = apply_threshold(scores, threshold)

    error_rows = []
    for row, pred in zip(rows, preds):
        error_row = dict(row)
        error_row["pred"] = int(pred)
        error_row["distance_to_threshold"] = abs(row["score"] - threshold)
        error_rows.append(error_row)

    false_positives = [
        row
        for row in error_rows
        if row["label"] == 0
        and row["pred"] == 1
        and row["distance_to_threshold"] <= boundary_window
    ]
    false_negatives = [
        row
        for row in error_rows
        if row["label"] == 1
        and row["pred"] == 0
        and row["distance_to_threshold"] <= boundary_window
    ]

    false_positives.sort(key=lambda row: row["distance_to_threshold"])
    false_negatives.sort(key=lambda row: row["distance_to_threshold"])

    print(f"Threshold: {threshold}")
    print(f"Boundary window: {boundary_window}")
    print()

    print("Slice 1: False positives near the decision boundary")
    print(f"Count: {len(false_positives)}")
    for row in false_positives[: args.top_k]:
        print(
            f'left={row["left_path"]}, right={row["right_path"]}, '
            f'label={row["label"]}, pred={row["pred"]}, '
            f'score={row["score"]:.4f}, dist_to_threshold={row["distance_to_threshold"]:.4f}'
        )

    print()
    print("Slice 2: False negatives near the decision boundary")
    print(f"Count: {len(false_negatives)}")
    for row in false_negatives[: args.top_k]:
        print(
            f'left={row["left_path"]}, right={row["right_path"]}, '
            f'label={row["label"]}, pred={row["pred"]}, '
            f'score={row["score"]:.4f}, dist_to_threshold={row["distance_to_threshold"]:.4f}'
        )


if __name__ == "__main__":
    main()