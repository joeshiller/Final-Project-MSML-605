from loguru import logger

# from msml605.load_data import download_dataset
from msml605 import load_data, manifest


def main():
    logger.info("Starting LFW ingestion")
    hugging_face_handle = "jessicali9530/lfw-dataset"
    input_dir = "input-data"
    output_dir = "output-data"
    load_data.download_dataset(hugging_face_handle, input_dir)
    raw = load_data.load_dataset(input_dir)
    train, val, test = load_data.split_dataset(raw, output_dir)

    seed = 1234
    man = manifest.Manifest(
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
        data_source=manifest.DataSource(
            url=hugging_face_handle, version="kagglehub", cache_dir=input_dir
        ),
    )

    logger.debug(man)

    manifest.write_manifest(man, f"{output_dir}/manifest.json")


if __name__ == "__main__":
    main()
