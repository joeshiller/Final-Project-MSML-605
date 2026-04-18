import argparse
import csv
import random
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from loguru import logger

from msml605 import config, pairs, run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    logger.info("Starting deterministic pair generation")

    # Either take the users config or the default path.
    env_cfg = config.load_environment_config(config.environment_config_path)
    run_model = run.get_run(env_cfg, args.run)

    cfg = run_model.load_config(env_cfg)
    run_dir = run_model.get_path(env_cfg)

    summaries = []
    for split in ["train", "val", "test"]:
        summaries.append(
            pairs.generate_pairs_for_split(cfg.pair_policy, run_dir, cfg.seed, split)
        )

    for summary in summaries:
        logger.info(summary)


if __name__ == "__main__":
    main()
