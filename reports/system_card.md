# System Card: LFW Face Verification System

## 1. System Overview

This project implements a face verification system for the LFW dataset. Given two face images, the system predicts whether the images are likely to show the same identity.

The final system uses an embedding-based pipeline:

1. Load two input images

2. Preprocess both images deterministically

3. Generate one embedding per image using `InceptionResnetV1` from `facenet-pytorch`

4. Compute Euclidean distance between the embeddings

5. Apply the selected operating threshold

6. Return a same/different prediction, confidence value, and latency


## 2. Intended Use

This system is intended for educational face verification on the LFW dataset. It is designed to demonstrate deterministic data processing, embedding-based inference, threshold selection, CLI inference, and Docker.

## 3. Out-of-Scope Uses
This system should not be used for real-world identity verification or any high-stakes decision-making. It has not been validated for those settings.

## 4. Data Summary
The system uses the LFW dataset. The project creates deterministic positive and negative face-verification pairs using seed `123`.

The final pair policy is a 1000|200|200 split:

- train: 1000 positive pairs and 1000 negative pairs

- validation: 200 positive pairs and 200 negative pairs

- test: 200 positive pairs and 200 negative pairs

- caps on positive candidate pairs per identity

## Important data limitations:

1. The dataset we are using may not represent all demographic groups equally

2. The project does not include reliable demographic metadata

3. The performance on LFW does not guarantee performance on any real-world images


## 5. Final Operating Threshold and Metrics

- The final system is using Euclidean distance between embeddings. A Lower score means that the pair is more likely to show the same identity. 
- Final operating threshold: `0.9010818501551252`
The threshold was selected by maximizing balanced accuracy on the validiaton split.
Prediction rule:
- If `distance <= 0.9010818501551252`, predict the same identity
- Else, predict different identities.

The validation metrics at the selected threshold:

| Metric | Value |
| Accuracy | `0.9825` |
| Balanced accuracy | `0.9825` |
| True positives | `195` |
| True negatives | `198` |
| False positives | `2` |
| False negatives | `5` |

| Actually Positive | Actually Negative |
| Predicted Positive | 195 | 2 |
| Predicted Negative | 5 | 198 |

## 6. Failure Modes and Limitations

This system may be less reliable when:

- faces are blurry, cropped, low resolution, or have bad lighting
- faces are partially occluded
- faces appear at unusual angles or poses
- the two images have huge differences in age, expression, lighting, or image quality
- different people that look visually similar
- the same person appears under very different imaging conditions.

The confidence score is based on distance from the selected threshold. It should not be interpreted as a calibrated probability.

## 7. Fairness-Related Risks and Misuse Concerns

Some of the misuse could create privacy, surveillance, or discrimination risks, since this is face verification. This project does not include reliable demographic labels, so it does not make any claims about equal performance across demographic groups.

Potential fairness-related risks

- different performance across groups if the dataset or model represents some populations better than others

- lower reliability for images with different lighting, pose, age, or quality

- harmful use in high-stakes identity decisions without proper validatio

This system should be treated as an educational prototype

## 8. Operational Constraints

The system assumes:

- input images are available in the LFW path format

- the environment has the required Python dependencies

- the CLI is run with the final threshold

- Docker or `uv` commands are used as documented in the README

## 9. Reproducibility Pointer

The final release can be reproduced using the commands in the README 

Supporting docs:

- `README.md`

- `configs/final_config.json`

- `reports/system_card.md`

- `reports/profiling.md`

- `reports/`