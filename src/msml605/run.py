import datetime
import glob
import hashlib
import os
import subprocess
import uuid
from pathlib import Path

from loguru import logger
from pydantic import BaseModel

import msml605.config


class RunConfig(BaseModel):
    split: str
    "What split (validation,test,train) was this run on?"

    threshold_rule: str

    threshold_value: float


class RunMetrics(BaseModel):
    accuracy: float
    balanced_accuracy: float
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int


class Run(BaseModel):
    id: uuid.UUID
    "Run Identifier (UUID4)"

    timestamp: datetime.datetime
    "The time the run was started, in the timezone UTC."

    commit_hash: str
    config: msml605.config.Config

    data_version: str
    "SHA256 hash of the CSVs in the output directory."

    threshold_info: RunConfig

    metrics: RunMetrics

    change_description: str
    "What changed?"


def create_run(
    config: msml605.config.Config,
    threshold_info: RunConfig,
    metrics: RunMetrics,
    change_description: str,
) -> Run:
    return Run(
        id=uuid.uuid4(),
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        commit_hash=get_git_commit_hash(),  # TODO: check if there are any staged changes.
        config=config,
        data_version=get_fingerprint_of_data(config),
        threshold_info=threshold_info,
        metrics=metrics,
        change_description=change_description,
    )


def get_git_commit_hash() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def get_fingerprint_of_file(file: Path, hash) -> None:
    # TODO: I don't know how to buffer with 'open' properly lol.
    # 65536 = 64KiB = 2^16 bytes.
    with open(file, "rb", buffering=65536) as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hash.update(data)


def get_fingerprint_of_data(config: msml605.config.Config) -> str:
    out_dir = config.output_dir
    csvs = glob.glob(f"{out_dir}/*.csv")
    hash = hashlib.sha256()
    for csv in csvs:
        get_fingerprint_of_file(csv, hash)
    hash_dig = hash.hexdigest()
    return hash_dig


def write_run(run: Run, run_dir: Path) -> str:
    "Writes the run. Returns the path of the file that was written."
    # Create all directories up to the file.
    os.makedirs(run_dir, exist_ok=True)

    id = run.id
    out_file_name = f"run_{str(id)}.json"
    out_file_path = run_dir / out_file_name

    if os.path.exists(out_file_path):
        logger.error("Run file already exists!", out_file_path=out_file_path)
        raise Exception("Run file already exists.")

    with open(out_file_path, "w") as file:
        serial_run = run.model_dump_json()
        file.write(serial_run)
    return out_file_path
