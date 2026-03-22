from pydantic import BaseModel
import datetime
import uuid
import .config
from pathlib import Path

class Run(BaseModel):
    id : uuid.UUID
    "Run Identifier (UUID4)"

    Timestamp : datetime.datetime
    "The time the run was started, in the timezone UTC."

    commit_hash : str
    config : config.Config

    data_version : str # TODO(David): what? Like just an incrementing number? Or the UUID for a generation (manifest.json) maybe?
    "Shows whether the pair data stayed fixed or changed."

    threshold_info : str # TODO: Like, is this just the threshold? Isn't that in the config?

    metrics : str # TODO: How well did the run go? Did it produce garbage?

    change_description : str
    "What changed?"

def create_run(config:Config, change_description:str)->Run:
    return Run(
        id = uuid.uuid4(),
        timestamp = datetime.datetime.now(datetime.timezone.utc),
        commit_hash = "TODO", # TODO: get the commit hash. also check if there are any staged changes.
        config = config,

        data_version = "todo", # incomplete.
        threshold_info = "todo",
        metrics = "very well",
        change_description= change_description
    )

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RUN_DIR = PROJECT_ROOT / "runs"

def write_run(run:Run)->None:
    pass
