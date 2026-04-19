import argparse
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np

from msml605 import config
from msml605.inference import verify_pair


def load_pairs_csv(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def run_one_pair(row, image_root, threshold, confidence_scale):
    return verify_pair(
        image_a_path=row["left_path"],
        image_b_path=row["right_path"],
        image_root=image_root,
        threshold=threshold,
        confidence_scale=confidence_scale,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", required=True, choices=["val", "test"])
    parser.add_argument("--num-pairs", type=int, default=20)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--threshold", type=float, required=True)
    parser.add_argument("--confidence-scale", type=float, default=1.0)
    args = parser.parse_args()

    cfg = config.load_config(config.config_path)
    output_dir = Path(cfg.output_dir)
    image_root = Path(cfg.input_dir) / "lfw-deepfunneled" / "lfw-deepfunneled"

    pairs_path = output_dir / f"pairs_{args.split}.csv"
    rows = load_pairs_csv(pairs_path)[: args.num_pairs]

    latencies = []
    failures = 0
    successes = 0
    error_messages = []

    start_wall = time.perf_counter()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_row = {
            executor.submit(
                run_one_pair,
                row,
                image_root,
                args.threshold,
                args.confidence_scale,
            ): row
            for row in rows
        }

        for future in as_completed(future_to_row):
            row = future_to_row[future]
            try:
                result = future.result()
                latencies.append(result["latency_ms"])
                successes += 1
            except Exception as e:
                failures += 1
                message = (
                    f"request failed for pair "
                    f"{row['left_path']} vs {row['right_path']}: {e}"
                )
                error_messages.append(message)
                print(message)

    total_wall_time_sec = time.perf_counter() - start_wall

    if latencies:
        latencies_np = np.array(latencies, dtype=float)
        mean_latency_ms = float(np.mean(latencies_np))
        p95_latency_ms = float(np.percentile(latencies_np, 95))
    else:
        mean_latency_ms = 0.0
        p95_latency_ms = 0.0

    throughput = successes / total_wall_time_sec if total_wall_time_sec > 0 else 0.0

    summary = {
        "split": args.split,
        "num_pairs_requested": len(rows),
        "workers": args.workers,
        "successful_requests": successes,
        "failed_requests": failures,
        "total_wall_time_sec": total_wall_time_sec,
        "throughput_requests_per_sec": throughput,
        "mean_latency_ms": mean_latency_ms,
        "p95_latency_ms": p95_latency_ms,
        "errors": error_messages,
    }

    print(json.dumps(summary, indent=2))

    summary_path = output_dir / "load_test_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()