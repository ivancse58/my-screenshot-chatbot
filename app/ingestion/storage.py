# Author: ChatGPT
import sqlite3

import pillow_heif

from app.config import DB_PATH

# Register HEIF opener so PIL can open .heic images
pillow_heif.register_heif_opener()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# Initialize DB if it doesn't exist
def init_db():
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                file_name TEXT,
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


# Insert image data into the SQLite database
def insert_image_data(file_hash, file_name, text):
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO images (id, file_name, text) VALUES (?, ?, ?)",
            (file_hash, file_name, text)
        )
        conn.commit()


# Check if a file has already been processed
def is_already_processed(file_hash):
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM images WHERE id=?", (file_hash,))
        return cursor.fetchone() is not None


# Call DB initialization on module import
init_db()
