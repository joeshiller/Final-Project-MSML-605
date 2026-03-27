import uuid
from pathlib import Path

import pytest

from msml605 import config, load_data, manifest, pairs


def test_integrate():
    cfg = config.load_config("tests/config.json")

    # ingest data
    raw = load_data.load_dataset(cfg.input_dir)
    train, val, test = load_data.split_dataset(raw, cfg.output_dir)

    seed = cfg.seed
    man = manifest.DataManifest(
        id=uuid.uuid4(),
        seed=seed,
        split_policy="identity",
        counts=[
            [
                len(train),
                sum(train["images"]),
            ],
            [
                len(val),
                sum(val["images"]),
            ],
            [
                len(test),
                sum(test["images"]),
            ],
        ],
        data_source=manifest.DataSource(
            url="file://somewhere-lol", version="TEST", cache_dir=cfg.input_dir
        ),
    )

    manifest.write_manifest(man, f"{cfg.output_dir}/manifest.json")

    # make_pairs
    summaries = []
    for split in ["train", "val", "test"]:
        summaries.append(
            pairs.generate_pairs_for_split(
                cfg.pair_policy, Path(cfg.output_dir), cfg.seed, split
            )
        )
