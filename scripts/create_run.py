import argparse
import csv
import json
from pathlib import Path

import numpy as np
from loguru import logger

from msml605 import config, run
from msml605.metrics import apply_threshold, evaluate_predictions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("description")
    args = parser.parse_args()

    cfg = config.load_config(config.config_path)

    this_run = run.create_run(
        cfg,
        args.description,
    )

    run_path = run.write_run(this_run, cfg.get_run_dir())

    logger.info(f"Wrote run to {run_path}")


if __name__ == "__main__":
    main()
