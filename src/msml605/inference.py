import time
from pathlib import Path

import numpy as np

from msml605.metrics import apply_threshold
from msml605.scoring import load_image_vector
from msml605.similarity import euclidean_distance_batch
from msml605.confidence import compute_confidence


def verify_pair(
    image_a_path: str,
    image_b_path: str,
    image_root: Path,
    threshold: float,
    confidence_scale: float = 1.0,
):
    start = time.perf_counter()

    left_vector = load_image_vector(image_a_path, image_root)
    right_vector = load_image_vector(image_b_path, image_root)

    left_vectors = np.expand_dims(left_vector, axis=0)
    right_vectors = np.expand_dims(right_vector, axis=0)

    score = float(euclidean_distance_batch(left_vectors, right_vectors)[0])
    decision_num = int(apply_threshold(np.array([score]), threshold)[0])
    decision = "same" if decision_num == 1 else "different"
    confidence = compute_confidence(score, threshold, scale=confidence_scale)

    latency_ms = (time.perf_counter() - start) * 1000.0

    return {
        "image_a": image_a_path,
        "image_b": image_b_path,
        "score": score,
        "threshold": float(threshold),
        "decision": decision,
        "confidence": confidence,
        "latency_ms": latency_ms,
    }