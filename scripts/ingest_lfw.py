from loguru import logger

# from msml605.load_data import download_dataset
from msml605 import load_data


def main():
    logger.info("Starting LFW ingestion")
    load_data.download_dataset()
    raw = load_data.load_dataset()
    stuff = load_data.split_dataset(raw)


if __name__ == "__main__":
    main()
