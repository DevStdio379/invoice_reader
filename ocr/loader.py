# ocr/loader.py
import io
from PIL import Image
from pdf2image import convert_from_bytes

POPPLER_PATH = r"C:\poppler-25.11.0\Library\bin"

def load_document(file_bytes: bytes):
    """
    Accept raw bytes of an image or PDF; return PIL.Image (RGB).
    For PDFs, we convert the FIRST page to an image.
    """

    # for PDF files
    if file_bytes[:4] == b"%PDF":
        pages = convert_from_bytes(file_bytes, dpi=300)

        if not pages:
            raise ValueError("No pages found in PDF.")
        
        return pages[0].convert("RGB")
    # for IMAGE files
    else:
        return Image.open(io.BytesIO(file_bytes)).convert("RGB")
    