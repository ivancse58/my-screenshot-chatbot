# Author: ChatGPT
import os
import time

import pillow_heif
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from app.config import WATCH_FOLDER
from app.indexing.id_map import load_id_map, save_id_map
from app.indexing.index import load_index, save_index
from app.ingestion.embedder import get_embedding
from app.ingestion.ocr import extract_text_from_image
from app.ingestion.storage import insert_image_data, is_already_processed
from app.utils.hashing import generate_file_hash
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
index = load_index(384)  # Embedding size for MiniLM
id_map = load_id_map()

# Register HEIF handler
pillow_heif.register_heif_opener()


class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith(
                ('.PNG', '.JPG', '.png', '.jpg', '.jpeg', '.heic')):
            return

        logger.info(f"New file detected: {event.src_path}")
        if event.src_path.lower().endswith('.heic'):
            logger.info(f"Handling --------------HEIC--------- image")
        process_image(event.src_path)


def process_image(image_path):
    # Handle HEIC automatically with pillow-heif
    # ext = os.path.splitext(image_path)[-1].lower()
    try:
        file_hash = generate_file_hash(image_path)
        if is_already_processed(file_hash):
            logger.info(f"Skipped already processed file: {image_path}")
            return

        text = extract_text_from_image(image_path)
        if not text.strip():
            logger.warning(f"No extractable text in: {image_path}")
            return

        insert_image_data(file_hash, os.path.basename(image_path), text)
        embedding = get_embedding(text)
        index.add(embedding)
        id_map.append(file_hash)

        save_index(index)
        save_id_map(id_map)

        logger.info(f"Successfully processed and indexed: {image_path}")
    except Exception as e:
        logger.error(f"Failed to process {image_path}: {e}")


def start_watcher():
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    observer = Observer()
    observer.schedule(ImageHandler(), WATCH_FOLDER, recursive=False)
    observer.start()
    logger.info("Started watching folder for new images.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping folder watcher...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_watcher()
