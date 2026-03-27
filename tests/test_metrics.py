import numpy as np
import pytest

import msml605.metrics


def test_apply_threshold():
    assert (
        msml605.metrics.apply_threshold([1, 3], 2) == np.asarray([1, 0], dtype=int)
    ).all()


def test_confusion_counts():
    assert msml605.metrics.confusion_counts([1, 0, 1], [0, 0, 1]) == {
        "tp": 1,
        "tn": 1,
        "fp": 0,
        "fn": 1,
    }


def test_accuracy():
    assert msml605.metrics.accuracy([1, 0, 1], [0, 0, 1]) == (2 / 3)


def test_balanced_accuracy_from_counts():
    assert (
        msml605.metrics.balanced_accuracy_from_counts(4, 5, 6, 7) == 0.40909090909090906
    )


def test_balanced_accuracy():
    assert msml605.metrics.balanced_accuracy([1, 0, 0, 1], [1, 1, 0, 1]) == 0.75


def test_evaluate_predicitions():
    assert msml605.metrics.evaluate_predictions([1, 0, 0, 1], [1, 1, 0, 1]) == {
        "accuracy": 0.75,
        "balanced_accuracy": 0.75,
        "fn": 0,
        "fp": 1,
        "tn": 1,
        "tp": 2,
    }
