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
    # TODO: allow the user to specify their own config path or config as a string.
    # Or the env config.
    args = parser.parse_args()

    # Either take the users config or the default path.
    env_cfg = config.load_environment_config(config.environment_config_path)

    this_run = run.create_run(
        # cfg,
        args.description,
    )
    this_run_path = env_cfg.get_run_dir() / f"run_{this_run.id}"

    run_path = run.write_run(this_run, env_cfg.get_run_dir())

    logger.info(f"Wrote run to {run_path}")

    # copy the config to the run
    with open(config.config_path, "r") as cfg_file:
        cfg = cfg_file.read()
        with open(this_run_path / "config.json", "w") as new_cfg_file:
            new_cfg_file.write(cfg)
    logger.info(f"Wrote config to {this_run_path / 'config.json'}")

    # somehow create a new file descriptor output and write to it.
    logger.info(f"Run ID is {this_run.id}")


if __name__ == "__main__":
    main()
