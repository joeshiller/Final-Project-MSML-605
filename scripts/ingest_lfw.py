import uuid
from pathlib import Path

from loguru import logger

from msml605 import config, load_data, manifest


def main():
    logger.info("Starting LFW ingestion")
    hugging_face_handle = "jessicali9530/lfw-dataset"
    cfg = config.load_config(config.config_path)

    load_data.download_dataset(hugging_face_handle, cfg.input_dir)
    raw = load_data.load_dataset(cfg.input_dir)
    # train, val, test = load_data.split_dataset(raw, cfg.output_dir)
    data_source = manifest.DataSource(
        url=hugging_face_handle, version="kagglehub", cache_dir=cfg.input_dir
    )

    logger.debug(data_source)
    # TODO(David): store data source in output-data/data-source.json

    # seed = cfg.seed
    # man = manifest.DataManifest(
    #     id=uuid.uuid4(),
    #     seed=seed,
    #     split_policy="identity",
    #     counts=[
    #         [
    #             len(train),
    #             sum(train["images"]),
    #         ],
    #         [
    #             len(val),
    #             sum(val["images"]),
    #         ],
    #         [
    #             len(test),
    #             sum(test["images"]),
    #         ],
    #     ],
    #     data_source=manifest.DataSource(
    #         url=hugging_face_handle, version="kagglehub", cache_dir=cfg.input_dir
    #     ),
    # )

    # logger.debug(man)

    # manifest.write_manifest(man, f"{cfg.output_dir}/manifest.json")


if __name__ == "__main__":
    main()
