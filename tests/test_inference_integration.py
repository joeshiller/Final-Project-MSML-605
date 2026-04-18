from pathlib import Path

from msml605 import config
from msml605.inference import verify_pair


def test_smoke_verify_pair_runs_end_to_end():
    cfg = config.load_config(config.config_path)
    image_root = Path(cfg.input_dir) / "lfw-deepfunneled" / "lfw-deepfunneled"

    result = verify_pair(
        image_a_path="Al_Pacino/Al_Pacino_0001.jpg",
        image_b_path="Al_Pacino/Al_Pacino_0002.jpg",
        image_root=image_root,
        threshold=0.9512748293069379,
        confidence_scale=1.0,
    )

    assert result["image_a"] == "Al_Pacino/Al_Pacino_0001.jpg"
    assert result["image_b"] == "Al_Pacino/Al_Pacino_0002.jpg"
    assert isinstance(result["score"], float)
    assert result["decision"] in {"same", "different"}
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["latency_ms"] >= 0.0