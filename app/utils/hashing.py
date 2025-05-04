# Author: ChatGPT
import hashlib


def generate_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
