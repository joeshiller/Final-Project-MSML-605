import time
from math import sqrt

import numpy as np
from loguru import logger

# def mag(a) -> float:
# return sqrt(sum(x**2 for x in a))
# for x in len(a)


def cosine_sim(a, b):
    # dot = sum(a * b for a, b in zip(a, b))
    # return dot / (mag(a) * mag(b))
    sum = 0
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            sum += a[x, y] * b[x, y]
    mags = np.linalg.norm(a) * np.linalg.norm(b)
    return sum / mags


def euclidean_sim(a,b):
    total = 0
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            diff = a[x, y] - b[x, y]
            total += diff * diff
    return total**0.5
   
            
        

def main():
    logger.info("Hello from benchmark.py")
    n = 1000
    d = 2000
    rng = np.random.default_rng()
    # Generate a 1D array of 5 random floats
    random_floats_a = rng.random(size=(n, d))
    random_floats_b = rng.random(size=(n, d))
    # logger.info(random_floats)

    logger.info("cosine sim - python")
    start = time.perf_counter()

    cosine_python = cosine_sim(random_floats_a, random_floats_b)

    end = time.perf_counter()
    cosine_python_dt = end - start
    logger.info(f"cosine sim - python - {cosine_python_dt:.6f}")

    logger.info("euclidean sim - python")
    start = time.perf_counter()
    euclidean_python = euclidean_sim(random_floats_a, random_floats_b)
    end = time.perf_counter()
    euclidean_python_dt = end - start
    logger.info(f"euclidean sim - python - {euclidean_python_dt:.6f}")
    logger.info(f"euclidean value - {euclidean_python}")


if __name__ == "__main__":
    main()
