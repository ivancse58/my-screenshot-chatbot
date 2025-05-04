# Author: ChatGPT
import os

import faiss

from app.config import INDEX_PATH


def load_index(dim):
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    else:
        return faiss.IndexFlatL2(dim)


def save_index(index):
    faiss.write_index(index, INDEX_PATH)
