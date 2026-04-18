from msml605.confidence import compute_confidence


def test_confidence_threshold():
    threshold = 1.0

    near = compute_confidence(0.95, threshold, scale=1.0)
    far = compute_confidence(0.20, threshold, scale=1.0)

    assert 0.0 <= near <= 1.0
    assert 0.0 <= far <= 1.0
    assert far > near