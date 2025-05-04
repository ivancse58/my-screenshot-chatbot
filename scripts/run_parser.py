# Author: ChatGPT
import os
import time

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
index = load_index(384)  # Depends on embedding model
id_map = load_id_map()


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith((".png", ".jpg", ".jpeg")):
            return

        file_hash = generate_file_hash(event.src_path)
        if is_already_processed(file_hash):
            logger.info(f"Already processed: {event.src_path}")
            return

        text = extract_text_from_image(event.src_path)
        if not text:
            logger.warning(f"No text in: {event.src_path}")
            return

        insert_image_data(file_hash, os.path.basename(event.src_path), text)
        emb = get_embedding(text)
        index.add(emb)
        id_map.append(file_hash)
        save_index(index)
        save_id_map(id_map)
        logger.info(f"Processed and indexed: {event.src_path}")


if __name__ == "__main__":
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    observer = Observer()
    observer.schedule(Handler(), WATCH_FOLDER, recursive=False)
    observer.start()
    logger.info("Watching folder for new images...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
