import numpy as np
from loguru import logger


def cosine_sim(a: list[float], b: list[float]):
    pass


def euclidan_sim(a: list[float], b: list[float]):
    pass


def main():
    logger.info("Hello from benchmark.py")
    n = 100
    d = 200
    rng = np.random.default_rng()
    # Generate a 1D array of 5 random floats
    random_floats = rng.random(size=(n, d))
    logger.info(random_floats)


if __name__ == "__main__":
    main()
