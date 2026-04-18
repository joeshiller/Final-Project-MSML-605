from pathlib import Path

from pydantic import BaseModel

# from msml605.run import Run

# class PairPolicyEntry(BaseModel):
#     num_pos: int
#     num_neg: int


# class PairPolicy(BaseModel):
#     train: PairPolicyEntry
#     val: PairPolicyEntry
#     test: PairPolicyEntry


class EnvironmentConfig(BaseModel):
    "Liekly in 'configs/environment.json'"

    input_dir: str
    output_dir: str
    run_dir: str
    "Within the `Config.output_dir`."

    def get_run_dir(self) -> Path:
        return Path(self.output_dir) / self.run_dir


class Config(BaseModel):
    "Likely in 'configs/config.json'"

    seed: int
    pair_policy: dict[str, dict[str, int]]


PROJECT_ROOT = Path(__file__).resolve().parents[2]

config_path = PROJECT_ROOT / "configs" / "config.json"
environment_config_path = PROJECT_ROOT / "configs" / "environment.json"


def load_environment_config(path) -> EnvironmentConfig:
    with open(path, "r") as file:
        content = file.read()
        return EnvironmentConfig.model_validate_json(content)
