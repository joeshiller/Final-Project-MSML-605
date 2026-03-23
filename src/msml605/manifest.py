import hashlib
import os
import uuid

from pydantic import BaseModel


class DataSource(BaseModel):
    url: str
    version: str
    cache_dir: str


def get_dataset_fingerprint():
    return hashlib.sha256(b"todo: fix this!")  # TODO: fix this!


class DataManifest(BaseModel):
    "Description of how the data was generated."

    fingerprint: str = get_dataset_fingerprint().hexdigest()
    "Hash of all files in our dataset (csv file + referenced data [face images])."
    # Note: does not contain mainifest file.

    seed: int

    split_policy: str

    counts: list[
        list[int]
    ]  # like [[3 names, 3 images] in train, [4names, 5images] in validation, and [10 names, 10 images] in test]

    data_source: DataSource


def write_manifest(manifest: DataManifest, out_file_path: str):
    # Create all directories up to the file.
    os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

    with open(out_file_path, "w") as file:
        serial_manifest = manifest.model_dump_json()
        file.write(serial_manifest)
