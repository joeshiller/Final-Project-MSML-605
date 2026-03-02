import itertools
import math
import os

# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub

# import cs
import pandas as pd
from kagglehub import KaggleDatasetAdapter

# import polars as pl
# import mlcroissant as mlc
# import tensorflow_datasets as tfds
from loguru import logger


def download_dataset(hugging_face_handle: str, output_dir: str):
    # Fetch the Croissant JSON-LD
    # croissant_dataset = mlc.Dataset(croissant_url)

    # Check what record sets are in the dataset
    # record_sets = croissant_dataset.metadata.record_sets
    # logger.debug("Downloaded metadata")
    # logger.debug(record_sets)

    # # Set the path to the file you'd like to load
    # for set in record_sets:
    #  Load the latest version
    _ = kagglehub.dataset_download(hugging_face_handle, output_dir=output_dir)
    # _ = kagglehub.dataset_download("jessicali9530/lfw-dataset", output_dir="input-data")


def load_dataset(input_dir: str):
    file_name = f"{input_dir}/lfw_allnames.csv"
    df = pd.read_csv(file_name).sort_values(by=["name", "images"])
    logger.debug(df.head())
    logger.debug(f"dataset is {len(df)} long.")
    return df


def split_dataset(df: pd.DataFrame, output_dir: str):
    # split policy is hard-coded as per-identity.
    #
    #  train/val/test
    # 70/15/15
    train_perc = 0.70
    val_perc = 0.15
    test_perc = 1 - math.floor(train_perc + val_perc)

    row_count = len(df)
    train_end = math.floor(row_count * train_perc)
    train_df = df.iloc[0:train_end]

    val_end = math.floor(train_end + row_count * val_perc)
    val_df = df.iloc[train_end:val_end]

    test_end = math.floor(val_end + row_count * test_perc)
    test_df = df.iloc[val_end:test_end]

    logger.debug(f"train set size : {len(train_df)}")
    # logger.debug(f"train set head : {train_df.head()}")
    # logger.debug(f"train set head : {train_df.tail()}")
    logger.debug(f"val set size : {len(val_df)}")
    # logger.debug(f"val set head : {val_df.head()}")
    # logger.debug(f"val set tail : {val_df.tail()}")
    logger.debug(f"test set size : {len(test_df)}")
    # logger.debug(f"test set head : {test_df.head()}")
    # logger.debug(f"test set tail : {test_df.tail()}")

    logger.debug(
        f"sum of everything : {sum([len(train_df), len(val_df), len(test_df)])}"
    )

    # Create all directories up to the file.
    os.makedirs(output_dir, exist_ok=True)

    train_df.to_csv(f"{output_dir}/train_identities.csv", index=False)
    val_df.to_csv(f"{output_dir}/val_identities.csv", index=False)
    test_df.to_csv(f"{output_dir}/test_identities.csv", index=False)
    return (train_df, val_df, test_df)
