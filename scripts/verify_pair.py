import argparse
import json
from pathlib import Path

from msml605 import config
from msml605.inference import verify_pair


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-a", required=True)
    parser.add_argument("--image-b", required=True)
    parser.add_argument("--threshold", type=float, required=True)
    parser.add_argument("--confidence-scale", type=float, default=1.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cfg = config.load_config(config.config_path)
    image_root = Path(cfg.input_dir) / "lfw-deepfunneled" / "lfw-deepfunneled"

    result = verify_pair(
        image_a_path=args.image_a,
        image_b_path=args.image_b,
        image_root=image_root,
        threshold=args.threshold,
        confidence_scale=args.confidence_scale,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"image_a: {result['image_a']}")
        print(f"image_b: {result['image_b']}")
        print(f"score: {result['score']:.4f}")
        print(f"threshold: {result['threshold']:.4f}")
        print(f"decision: {result['decision']}")
        print(f"confidence: {result['confidence']:.4f}")
        print(f"latency_ms: {result['latency_ms']:.2f}")


if __name__ == "__main__":
    main()