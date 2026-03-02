from pathlib import Path

SEED = 123

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

PAIR_POLICY = {
    "train": {"num_pos": 1000, "num_neg": 1000},
    "val": {"num_pos": 200, "num_neg": 200},
    "test": {"num_pos": 200, "num_neg": 200},
}