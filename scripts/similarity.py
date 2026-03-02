import numpy as np


def _validate_inputs(a,b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if a.ndim != 2 or b.ndim != 2:
        raise ValueError("a and b must both have shape (N, D)")

    if a.shape != b.shape:
        raise ValueError(f"a and b must have the same shape")

    return a, b

#cos(theta) =  a * b / |a||b|
def cosine_similarity_batch(a, b, eps=1e-12):

    a, b = _validate_inputs(a, b)

    dot_products = np.sum(a * b, axis=1)
    a_norms = np.linalg.norm(a, axis=1)
    b_norms = np.linalg.norm(b, axis=1)

    denom = np.maximum(a_norms * b_norms, eps)
    return dot_products / denom


def euclidean_distance_batch(a,b):
    a, b = _validate_inputs(a, b)
    return np.linalg.norm(a - b, axis=1)