from PIL import Image
import pytesseract
import os


def extract_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

