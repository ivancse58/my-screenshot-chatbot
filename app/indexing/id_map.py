# Author: ChatGPT
import os
import pickle

from app.config import ID_MAP_PATH


def load_id_map():
    if os.path.exists(ID_MAP_PATH):
        with open(ID_MAP_PATH, "rb") as f:
            return pickle.load(f)
    return []


def save_id_map(id_map):
    with open(ID_MAP_PATH, "wb") as f:
        pickle.dump(id_map, f)
