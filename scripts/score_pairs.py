import csv
from pathlib import Path

import numpy as np
from loguru import logger
from PIL import Image

# from similarity import euclidean_distance_batch
from msml605 import config, scoring


def main():
    logger.info("Starting pair scoring")

    cfg = config.load_config(config.config_path)
    output_dir = Path(cfg.output_dir)
    image_root = Path(cfg.input_dir) / "lfw-deepfunneled" / "lfw-deepfunneled"

    split = "val"
    pairs_path = output_dir / f"pairs_{split}.csv"
    scores_path = output_dir / f"{split}_scores.csv"

    rows = scoring.load_pairs_csv(pairs_path)
    scores = scoring.score_pairs(rows, image_root, image_size=64)
    scoring.write_scores_csv(scores_path, rows, scores)

    logger.info(f"Saved scored pairs to {scores_path}")


if __name__ == "__main__":
    main()
