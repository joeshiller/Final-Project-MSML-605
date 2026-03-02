import os

from pydantic import BaseModel


class DataSource(BaseModel):
    url: str
    version: str
    cache_dir: str


class Manifest(BaseModel):
    seed: int
    split_policy: str
    counts: list[
        list[int]
    ]  # like [[3 names, 3 images] in train, [4names, 5images] in validation, and [10 names, 10 images] in test]
    data_source: DataSource


def write_manifest(manifest: Manifest, out_file_path: str):
    # Create all directories up to the file.
    os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

    with open(out_file_path, "w") as file:
        serial_manifest = manifest.model_dump_json()
        file.write(serial_manifest)
