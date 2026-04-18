import argparse
import uuid
from pathlib import Path

from loguru import logger

from msml605 import config, load_data, manifest, run


def main():
    logger.info("Starting Data Preprocessing")
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    # Either take the users config or the default path.
    env_cfg = config.load_environment_config(config.environment_config_path)
    run_model = run.get_run(env_cfg, args.run)

    cfg = run_model.load_config(env_cfg)
    run_dir = run_model.get_path(env_cfg)

    raw = load_data.load_dataset(env_cfg.input_dir)
    train, val, test = load_data.split_dataset(raw, run_dir)

    hugging_face_handle = "jessicali9530/lfw-dataset"

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
        # TODO: this should be in ingest_lfw
        data_source=manifest.DataSource(
            url=hugging_face_handle, version="kagglehub", cache_dir=env_cfg.input_dir
        ),
    )

    logger.debug(man)

    manifest.write_manifest(man, run_dir / "manifest.json")


if __name__ == "__main__":
    main()
