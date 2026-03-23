import datetime
import os
import uuid
from pathlib import Path

from loguru import logger
from pydantic import BaseModel

import msml605.config


class Run(BaseModel):
    id: uuid.UUID
    "Run Identifier (UUID4)"

    timestamp: datetime.datetime
    "The time the run was started, in the timezone UTC."

    commit_hash: str
    config: msml605.config.Config

    data_version: str  # TODO(David): what? Like just an incrementing number? Or the UUID for a generation (manifest.json) maybe?
    "Shows whether the pair data stayed fixed or changed."

    threshold_info: (
        str  # TODO: Like, is this just the threshold? Isn't that in the config?
    )

    metrics: str  # TODO: How well did the run go? Did it produce garbage?

    change_description: str
    "What changed?"


def create_run(config: msml605.config.Config, change_description: str) -> Run:
    return Run(
        id=uuid.uuid4(),
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        commit_hash="TODO",  # TODO: get the commit hash. also check if there are any staged changes.
        config=config,
        data_version="todo",  # incomplete.
        threshold_info="todo",
        metrics="very well",
        change_description=change_description,
    )


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
