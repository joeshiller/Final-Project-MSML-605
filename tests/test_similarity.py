import numpy as np

from msml605.similarity import euclidean_distance_batch


def test_distance_toy_embeddings():
    a = np.array([[0.0, 0.0], [1.0, 1.0]])
    b = np.array([[3.0, 4.0], [1.0, 2.0]])

    scores = euclidean_distance_batch(a, b)

    assert np.allclose(scores, np.array([5.0, 1.0]))