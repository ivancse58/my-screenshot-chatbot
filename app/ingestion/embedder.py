# Author: ChatGPT
import numpy as np
import pillow_heif
from sentence_transformers import SentenceTransformer

from app.config import MODEL_NAME

pillow_heif.register_heif_opener()

model = SentenceTransformer(MODEL_NAME)


def get_embedding(text):
    return np.array([model.encode(text)], dtype="float32")
