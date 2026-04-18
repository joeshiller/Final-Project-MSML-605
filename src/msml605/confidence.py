import math


def compute_confidence(score: float, threshold: float, scale: float = 1.0) -> float:
    margin = abs(score - threshold)
    confidence = 1.0 - math.exp(-margin / max(scale, 1e-12))
    return float(max(0.0, min(1.0, confidence)))