import itertools

import mlcroissant as mlc
from loguru import logger


def download_dataset(
    croissant_url: str = "https://www.kaggle.com/datasets/jessicali9530/lfw-dataset/croissant/download",
):
    # Fetch the Croissant JSON-LD
    croissant_dataset = mlc.Dataset(croissant_url)

    # Check what record sets are in the dataset
    record_sets = croissant_dataset.metadata.record_sets
    logger.debug("Downloaded data", record_sets=record_sets)

    # # Set the path to the file you'd like to load
    # file_path = ""

    # # Fetch the records
    # record_set = croissant_dataset.records(record_set=file_path)
    # logger.debug("First 5 records:", list(itertools.islice(record_set, 5)))
