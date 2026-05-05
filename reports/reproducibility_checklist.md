# Reproducibility Checklist

## Final Release Information

Final system version: Milestone 4 final release  

Final Git tag: `v1.0-final`  

Final config: `configs/final_config.json`  

Final threshold: `0.9010818501551252`  

Threshold selection split: validation  

Threshold selection rule: maximize balanced accuracy  

Final validation balanced accuracy: `0.98249`  

Final validation accuracy: `0.9825`  

Final run location: `fixed-runs/34355db8-e23a-4d08-8379-6581c2001aa7`

Validation confusion matrix:

| Actually Positive | Actually Negative |

| Predicted Positive | 195 | 2 |

| Predicted Negative | 5 | 198 |

## Required Artifacts

| Artifact | Location |

| README | `README.md` |

| Final config | `configs/final_config.json` |

| System Card | `reports/system_card.md` |

| Profiling report | `reports/profiling.md` |

| Reproducibility checklist | `reports/reproducibility_checklist.md` |

| Threshold sweep output | `output-data/threshold_sweep_val.csv` |

| Load-test summary | `output-data/load_test_summary.json` |

| Tracked runs | `fixed-runs/` |

## 1. Clone the Repository

git clone https://github.com/joeshiller/Final-Project-MSML-605.git

cd Final-Project-MSML-605

git checkout v1.0-final

## 2. Build the Docker Image
scripts/build-image.sh

## 3. Ingest LFW
scripts/run-container.sh uv run scripts/ingest_lfw.py

## 4. Generate Pairs
scripts/run-container.sh uv run scripts/make_pairs.py

- The pair generation uses seed 123 and the pair policy recorded in configs/final_config.json

## 5. Score the Validation Pairs
scripts/run-container.sh uv run scripts/score_pairs.py --split=val

## 6. Reproducing Threshold 
scripts/run-container.sh uv run scripts/thresholds.py final_reproducibility_check

- Expected Result
threshold = 0.9010818501551252
accuracy = 0.9825
balanced_accuracy = 0.98249
tp = 195
tn = 198
fp = 2
fn = 5

output-data/threshold_sweep_val.csv

## 7. CLI Inference
scripts/run-container.sh uv run --no-sync python scripts/verify_pair.py \
  --image-a George_W_Bush/George_W_Bush_0001.jpg \
  --image-b George_W_Bush/George_W_Bush_0002.jpg \
  --threshold 0.9010818501551252

## 8. Load Test
scripts/run-container.sh uv run --no-sync python scripts/load_test.py \
  --split val \
  --num-pairs 20 \
  --workers 4 \
  --threshold 0.9010818501551252

## 9. Testing
scripts/run-container.sh uv run pytest

## 10. Reports
- reports/system_card.md
- reports/profiling.md
- reports/reproducibility_checklist.md

