# Author: ChatGPT
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WATCH_FOLDER = os.path.join(BASE_DIR, "data", "watch")
DB_PATH = os.path.join(BASE_DIR, "data", "db", "images.db")
INDEX_PATH = os.path.join(BASE_DIR, "data", "index", "image_index.faiss")
ID_MAP_PATH = os.path.join(BASE_DIR, "data", "index", "id_map.pkl")
LOG_PATH = os.path.join(BASE_DIR, "logs", "system.log")

SUPPORTED_LANGUAGES = "eng+ben+tha"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
LLM_ENDPOINT = "http://localhost:11434/v1"
LLM_MODEL = "llama3.2"
