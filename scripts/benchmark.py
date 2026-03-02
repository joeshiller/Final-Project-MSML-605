import time
from math import sqrt
import json
from pathlib import Path

import numpy as np
from loguru import logger
from similarity import cosine_similarity_batch, euclidean_distance_batch

# def mag(a) -> float:
# return sqrt(sum(x**2 for x in a))
# for x in len(a)


def cosine_sim(a, b):
    res = []
    for x in range(a.shape[0]):
        dot = 0.0
        a_sq = 0.0
        b_sq = 0.0
        for y in range(a.shape[1]):
            dot += a[x, y] * b[x, y]
            a_sq += a[x, y] * a[x, y]
            b_sq += b[x, y] * b[x, y]
        denom = max((sqrt(a_sq)) * (sqrt(b_sq)),1e-12 )
        res.append(dot / denom)

    return np.array(res)


def euclidean_sim(a, b):
    res = []
    for x in range(a.shape[0]):
        total = 0.0
        for y in range(a.shape[1]):
            diff = a[x, y] - b[x, y]
            total += diff * diff
        res.append(sqrt(total))

    return np.array(res)
   
            
        

def main():
    logger.info("Hello from benchmark.py")
    n = 1000
    d = 2000
    rng = np.random.default_rng()
    # Generate a 1D array of 5 random floats
    random_floats_a = rng.random(size=(n, d))
    random_floats_b = rng.random(size=(n, d))
    # logger.info(random_floats)

    logger.info("cosine sim - python loop")
    start = time.perf_counter()
    cosine_python = cosine_sim(random_floats_a, random_floats_b)
    end = time.perf_counter()
    cosine_python_dt = end - start
    logger.info(f"cosine sim - python loop - {cosine_python_dt:.6f}")

    logger.info("cosine sim - numpy vectorized")
    start = time.perf_counter()
    cosine_numpy = cosine_similarity_batch(random_floats_a, random_floats_b)
    end = time.perf_counter()
    cosine_numpy_dt = end - start
    logger.info(f"cosine sim - numpy vectorized - {cosine_numpy_dt:.6f}")

    logger.info("euclidean sim - python loop")
    start = time.perf_counter()
    euclidean_python = euclidean_sim(random_floats_a, random_floats_b)
    end = time.perf_counter()
    euclidean_python_dt = end - start
    logger.info(f"euclidean sim - python loop - {euclidean_python_dt:.6f}")

    logger.info("euclidean sim - numpy vectorized")
    start = time.perf_counter()
    euclidean_numpy = euclidean_distance_batch(random_floats_a, random_floats_b)
    end = time.perf_counter()
    euclidean_numpy_dt = end - start
    logger.info(f"euclidean sim - numpy vectorized - {euclidean_numpy_dt:.6f}")

    cosine_max_abs_diff = float(np.max(np.abs(cosine_python - cosine_numpy)))
    euclidean_max_abs_diff = float(np.max(np.abs(euclidean_python - euclidean_numpy)))

    cosine_within_tolerance = cosine_max_abs_diff < 1e-9
    euclidean_within_tolerance = euclidean_max_abs_diff < 1e-9

    logger.info(f"cosine max abs diff - {cosine_max_abs_diff}")
    logger.info(f"euclidean max abs diff - {euclidean_max_abs_diff}")
    logger.info(f"cosine within tolerance - {cosine_within_tolerance}")
    logger.info(f"euclidean within tolerance - {euclidean_within_tolerance}")

    results = {
        "shape": {
            "N": n,
            "D": d,
        },
        "cosine": {
            "python_loop_time_sec": cosine_python_dt,
            "numpy_vectorized_time_sec": cosine_numpy_dt,
            "max_abs_diff": cosine_max_abs_diff,
            "within_tolerance": cosine_within_tolerance,
        },
        "euclidean": {
            "python_loop_time_sec": euclidean_python_dt,
            "numpy_vectorized_time_sec": euclidean_numpy_dt,
            "max_abs_diff": euclidean_max_abs_diff,
            "within_tolerance": euclidean_within_tolerance,
        },
    }

    output_dir = Path("output-data")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "benchmark_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
        f.write("\n")

    logger.info(f"saved benchmark results to {output_path}")


if __name__ == "__main__":
    main()
