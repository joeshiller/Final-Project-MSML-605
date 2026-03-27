import csv
import random
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from loguru import logger

from msml605 import config, pairs


def main():
    logger.info("Starting deterministic pair generation")

    cfg = config.load_config(config.config_path)
    summaries = []
    for split in ["train", "val", "test"]:
        summaries.append(
            pairs.generate_pairs_for_split(
                cfg.pair_policy, Path(cfg.output_dir), cfg.seed, split
            )
        )

    for summary in summaries:
        logger.info(summary)


if __name__ == "__main__":
    main()
