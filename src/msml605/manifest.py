import hashlib
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel

import msml605.config


class DataSource(BaseModel):
    url: str
    version: str
    cache_dir: str
    fingerprint: str
    "Hash of the data files from the Internet"

    def __init__(self, /, **data: Any) -> None:
        data["fingerprint"] = get_fingerprint_of_dir(data["cache_dir"]).hexdigest()
        super().__init__(**data)


def get_fingerprint_of_dir(dir: Path):
    hash = hashlib.sha256()

    # BUF_SIZE is totally arbitrary
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    # get the files in the input data
    for dir_path, dir_names, file_names in os.walk(dir, topdown=True):
        # Modified from source - https://stackoverflow.com/a/22058673
        # Posted by Randall Hunt, modified by community. See post 'Timeline' for change history
        # Retrieved 2026-03-24, License - CC BY-SA 4.0
        for file_name in file_names:
            # read file contents.
            fqn_file_name = os.path.join(dir_path, file_name)
            with open(fqn_file_name, "rb") as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    hash.update(data)
    return hash


class DataManifest(BaseModel):
    "Description of how the data was generated."

    # fingerprint: str
    # "Hash of all files in our dataset (csv file + referenced data [face images])."
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
