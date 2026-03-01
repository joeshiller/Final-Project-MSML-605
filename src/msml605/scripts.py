from loguru import logger

from . import load_data


def bench_similarity():
    print("Hello from bench_similarity!")


def ingest_lfw():
    logger.info("Hello from ingest_lfw!")
    load_data.download_dataset()


def make_pairs():
    print("Hello from make_pairs!")
