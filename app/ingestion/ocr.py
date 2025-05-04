# Author: ChatGPT
import cv2
import numpy as np
import pillow_heif
import pytesseract
from PIL import Image

# Register HEIC format support
pillow_heif.register_heif_opener()


def extract_text_from_image(image_path):
    try:
        # Load image using PIL (pillow handles HEIC here)
        pil_image = Image.open(image_path)

        # Convert to OpenCV image (numpy array)
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Convert to grayscale for better OCR accuracy
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Run OCR
        text = pytesseract.image_to_string(gray)
        return text
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""
