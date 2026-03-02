from math import sqrt

import numpy as np
from loguru import logger


def mag(a: list[float]) -> float:
    return sqrt(sum(x**2 for x in a))


def cosine_sim(a: list[float], b: list[float]):
    dot = sum(a * b for a, b in zip(a, b))
    return dot / (mag(a) * mag(b))


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
