from loguru import logger

from msml605.load_data import download_dataset


def main():
    logger.info("Starting LFW ingestion")
    download_dataset()


if __name__ == "__main__":
    main()
