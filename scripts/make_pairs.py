import csv
import random
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from loguru import logger

from msml605 import config

# from msml605.config import OUTPUTS_DIR, PAIR_POLICY, SEED


def read_split_csv(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def expand_count_rows_to_paths(rows):
    expanded = []

    for row in rows:
        identity = row["name"]
        image_count = int(row["images"])

        for i in range(1, image_count + 1):
            image_path = f"{identity}/{identity}_{i:04d}.jpg"
            expanded.append(
                {
                    "identity": identity,
                    "image_path": image_path,
                }
            )

    return expanded


def group_by_identity(rows):
    grouped = defaultdict(list)

    for row in rows:
        grouped[row["identity"]].append(row["image_path"])

    identity_to_images = {}
    for identity in sorted(grouped.keys()):
        identity_to_images[identity] = sorted(grouped[identity])

    return identity_to_images


def build_positive_candidates(identity_to_images):
    candidates = []

    for identity in sorted(identity_to_images.keys()):
        images = identity_to_images[identity]
        if len(images) < 2:
            continue

        for left_path, right_path in combinations(images, 2):
            candidates.append((left_path, right_path, 1))

    return candidates


def build_negative_candidates(identity_to_images):
    candidates = []
    identities = sorted(identity_to_images.keys())

    for i in range(len(identities)):
        for j in range(i + 1, len(identities)):
            left_identity = identities[i]
            right_identity = identities[j]

            for left_path in identity_to_images[left_identity]:
                for right_path in identity_to_images[right_identity]:
                    candidates.append((left_path, right_path, 0))

    return candidates


def sample_candidates(candidates, num_needed, rng):
    if len(candidates) < num_needed:
        raise ValueError(
            f"Requested {num_needed} pairs but only found {len(candidates)} candidates"
        )

    sampled = rng.sample(candidates, num_needed)
    sampled.sort()
    return sampled


def write_pairs_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["left_path", "right_path", "label", "split"],
        )
        writer.writeheader()
        writer.writerows(rows)


def generate_pairs_for_split(pair_policy, output_dir, seed, split):
    input_path = output_dir / f"{split}_identities.csv"
    output_path = output_dir / f"pairs_{split}.csv"

    raw_rows = read_split_csv(input_path)
    expanded_rows = expand_count_rows_to_paths(raw_rows)
    identity_to_images = group_by_identity(expanded_rows)

    pos_candidates = build_positive_candidates(identity_to_images)
    neg_candidates = build_negative_candidates(identity_to_images)

    rng = random.Random(seed)

    pos_pairs = sample_candidates(
        pos_candidates,
        pair_policy[split]["num_pos"],
        rng,
    )
    neg_pairs = sample_candidates(
        neg_candidates,
        pair_policy[split]["num_neg"],
        rng,
    )

    all_rows = []
    for left_path, right_path, label in pos_pairs + neg_pairs:
        all_rows.append(
            {
                "left_path": left_path,
                "right_path": right_path,
                "label": label,
                "split": split,
            }
        )

    all_rows.sort(
        key=lambda row: (
            row["left_path"],
            row["right_path"],
            row["label"],
            row["split"],
        )
    )

    write_pairs_csv(output_path, all_rows)

    return {
        "split": split,
        "num_pairs": len(all_rows),
        "num_pos": pair_policy[split]["num_pos"],
        "num_neg": pair_policy[split]["num_neg"],
    }


def main():
    logger.info("Starting deterministic pair generation")

    cfg = config.load_config(config.config_path)
    summaries = []
    for split in ["train", "val", "test"]:
        summaries.append(
            generate_pairs_for_split(
                cfg.pair_policy, Path(cfg.output_dir), cfg.seed, split
            )
        )

    for summary in summaries:
        logger.info(summary)


if __name__ == "__main__":
    main()
