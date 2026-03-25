from pathlib import Path
import csv
from datetime import datetime
import subprocess


def get_git_commit_hash():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def log_run(row, output_path="output-data/run_summary.csv"):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "run_id",
        "timestamp",
        "commit_hash",
        "config_name",
        "data_version",
        "split",
        "threshold_rule",
        "threshold_value",
        "accuracy",
        "balanced_accuracy",
        "tp",
        "tn",
        "fp",
        "fn",
        "note",
    ]

    file_exists = path.exists()

    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)