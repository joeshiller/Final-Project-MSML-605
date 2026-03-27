from pathlib import Path
import csv

import numpy as np
from PIL import Image
from loguru import logger

from msml605 import config
from similarity import euclidean_distance_batch


def load_pairs_csv(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_image_vector(image_path, image_root, image_size):
    full_path = Path(image_root) / image_path
    image = Image.open(full_path).convert("L")
    image = image.resize((image_size, image_size))
    array = np.asarray(image, dtype=np.float32) / 255.0
    return array.reshape(-1)


def score_pairs(rows, image_root, image_size):
    left_vectors = []
    right_vectors = []

    for row in rows:
        left_vectors.append(load_image_vector(row["left_path"], image_root, image_size))
        right_vectors.append(load_image_vector(row["right_path"], image_root, image_size))

    left_vectors = np.stack(left_vectors, axis=0)
    right_vectors = np.stack(right_vectors, axis=0)

    scores = euclidean_distance_batch(left_vectors, right_vectors)
    return scores


def write_scores_csv(path, rows, scores):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["left_path", "right_path", "label", "split", "score"],
        )
        writer.writeheader()
        for row, score in zip(rows, scores):
            writer.writerow(
                {
                    "left_path": row["left_path"],
                    "right_path": row["right_path"],
                    "label": row["label"],
                    "split": row["split"],
                    "score": float(score),
                }
            )


def main():
    logger.info("Starting pair scoring")

    cfg = config.load_config(config.config_path)
    output_dir = Path(cfg.output_dir)
    image_root = Path(cfg.input_dir) / "lfw-deepfunneled" / "lfw-deepfunneled"

    split = "val"
    pairs_path = output_dir / f"pairs_{split}.csv"
    scores_path = output_dir / f"{split}_scores.csv"

    rows = load_pairs_csv(pairs_path)
    scores = score_pairs(rows, image_root, image_size=64)
    write_scores_csv(scores_path, rows, scores)

    logger.info(f"Saved scored pairs to {scores_path}")


if __name__ == "__main__":
    main()