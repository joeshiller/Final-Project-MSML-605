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