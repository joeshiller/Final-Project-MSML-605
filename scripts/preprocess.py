import uuid
from pathlib import Path

from loguru import logger

from msml605 import config, load_data, manifest, run


def main():
    logger.info("Starting Data Preprocessing")
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    cfg = config.load_config(config.config_path)

    run_model = run.get_run(cfg, args.run)

    seed = cfg.seed
    man = manifest.DataManifest(
        id=uuid.uuid4(),
        seed=seed,
        split_policy="identity",
        counts=[
            [
                len(train),
                sum(train["images"]),
            ],
            [
                len(val),
                sum(val["images"]),
            ],
            [
                len(test),
                sum(test["images"]),
            ],
        ],
        data_source=data_source,
    )

    logger.debug(man)

    manifest.write_manifest(man, f"{cfg.output_dir}/manifest.json")


if __name__ == "__main__":
    main()
