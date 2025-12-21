
import pytesseract
from PIL import Image

# ⭐ Tell Python exactly where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(img):
    try:
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error during OCR: {e}"
