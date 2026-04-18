import argparse
from pathlib import Path

import numpy as np
from loguru import logger
from PIL import Image

# from similarity import euclidean_distance_batch
from msml605 import config, run, scoring

# TODO: how do we know what run we are in?


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--split", required=True, choices=["train", "val", "test"])
    args = parser.parse_args()

    logger.info("Generating embeddings")

    # Either take the users config or the default path.
    env_cfg = config.load_environment_config(config.environment_config_path)
    run_model = run.get_run(env_cfg, args.run)

    cfg = run_model.load_config(env_cfg)
    run_dir = run_model.get_path(env_cfg)

    image_root = Path(env_cfg.input_dir) / "lfw-deepfunneled" / "lfw-deepfunneled"

    split = args.split
    pairs_path = run_dir / f"pairs_{split}.csv"
    embeddings_path = run_dir / f"{split}_embeddings.csv"

    rows = scoring.load_pairs_csv(pairs_path)
    embeddings = scoring.generate_embeddings(rows, image_root)
    scoring.write_embeddings_csv(embeddings_path, rows, embeddings)

    logger.info(f"Saved embeddings to {embeddings_path}")


if __name__ == "__main__":
    main()
