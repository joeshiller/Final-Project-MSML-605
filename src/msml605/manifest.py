class DataSource:
    url: str
    version: str
    cache_dir: str


class Manifest:
    seed: int
    split_policy: str
    counts: list[int]  # like [3 in train, 4 in validation, and 10 in test]
    data_source: DataSource
