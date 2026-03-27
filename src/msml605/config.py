from pathlib import Path

from pydantic import BaseModel

# class PairPolicyEntry(BaseModel):
#     num_pos: int
#     num_neg: int


# class PairPolicy(BaseModel):
#     train: PairPolicyEntry
#     val: PairPolicyEntry
#     test: PairPolicyEntry


class Config(BaseModel):
    seed: int
    input_dir: str
    output_dir: str
    run_dir: str
    "Within the `Config.output_dir`."
    pair_policy: dict[str, dict[str, int]]

    def get_run_dir(self) -> Path:
        return Path(self.output_dir) / self.run_dir


# SEED = 123

PROJECT_ROOT = Path(__file__).resolve().parents[2]
# INPUT_DIR = PROJECT_ROOT / "input-data"
# OUTPUTS_DIR = PROJECT_ROOT / "output-data"

# PAIR_POLICY = {
#     "train": {"num_pos": 1000, "num_neg": 1000},
#     "val": {"num_pos": 200, "num_neg": 200},
#     "test": {"num_pos": 200, "num_neg": 200},
# }

config_path = PROJECT_ROOT / "configs" / "config.json" #new config with data improvement


def load_config(path) -> Config:
    with open(path, "r") as file:
        content = file.read()
        return Config.model_validate_json(content)
