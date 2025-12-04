# ocr/preprocess.py
import cv2
import numpy as np
from PIL import Image

def preprocess(pil_img: Image.Image, scale_max= 1600):
    """
    Convert to grayscale, resize if small, denoise, adaptive threshold.
    Return a PIL.Image suitable for Tesseract.
    """

    arr = np.array(pil_img)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    # Resize (scale up) so the longer side is near scale_max if smaller
    h, w = gray.shape
    max_side = max(h, w)

    if max_side < scale_max:
        scale = scale_max / max_side
        new_w = int(w * scale)
        new_h = int(h * scale)
        gray = cv2.resize(gray, (new_w, new_h), interpolation = cv2.INTER_LINEAR)

    # Denoise and sharpen a bit
    gray = cv2.medianBlur(gray, 3)
    # Adaptive threshold for uneven illumination
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)

    return Image.fromarray(th)

    