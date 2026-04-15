import csv
from pathlib import Path

import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1

from loguru import logger
from PIL import Image
import gc

from msml605.similarity import euclidean_distance_batch

resnet = InceptionResnetV1(pretrained="vggface2").eval()

def load_pairs_csv(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def load_image_vector(image_path, image_root):
    full_path = Path(image_root) / image_path
    image = Image.open(full_path)
    array = np.asarray(image, dtype=np.float32) / 255.0
    img_tensor = torch.tensor(array)

    # This is a [255,255,3] tensor. we need a [3,255,255] tensor.
    img_tensor = torch.movedim(img_tensor,-1,0)
    embedding = resnet(img_tensor.unsqueeze(0))
   # Returns a 512-d array.
    return embedding.squeeze().detach().numpy()


def score_pairs(rows, image_root):
    left_vectors = []
    right_vectors = []
    logger.debug("Okay, about to start loading the embeddings.")

    for row in rows:
        left_vectors.append(load_image_vector(row["left_path"], image_root))
        right_vectors.append(
            load_image_vector(row["right_path"], image_root)
        )
    logger.debug("Finished loading up the embeddings")

    left_vectors = np.stack(left_vectors, axis=0)
    right_vectors = np.stack(right_vectors, axis=0)

    logger.debug("About to start calcing differences")
    scores = euclidean_distance_batch(left_vectors, right_vectors)
    logger.debug("Done calcing differences")
    return scores


def write_scores_csv(path, rows, scores):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["left_path", "right_path", "label", "split", "score"],
        )
        writer.writeheader()
        for row, score in zip(rows, scores):
            writer.writerow(
                {
                    "left_path": row["left_path"],
                    "right_path": row["right_path"],
                    "label": row["label"],
                    "split": row["split"],
                    "score": float(score),
                }
            )
