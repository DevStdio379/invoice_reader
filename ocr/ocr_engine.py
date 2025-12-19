# ocr.ocr_engine.py
from pytesseract import image_to_data, Output
from PIL import Image

def ocr_with_boxes(pil_img: Image.Image):
    """
    Run Tesseract OCR and return a list of words with bounding boxes (bbox) + normalized confidence (0..1).
    Each entry: {text, conf, left, top, width, height, line_num, block_num}
    """

    data = image_to_data(pil_img, output_type = Output.DICT)
    words = []
    n = len(data['text'])

    for i in range(n):
        txt = (data['text'][i] or "").strip()
        if not txt:
            continue

        # Tesseract returns confidence as string or '-1 for unknown

        try:
            conf_raw = float(data['conf'][i])
        except Exception:
            conf_raw = -1.0

        conf = max(0.0, min(1.0, conf_raw / 100.0)) if conf_raw >= 0 else 0.0
        words.append({

            "text": txt,
            "conf": conf,
            "left": int(data['left'][i]),
            "top": int(data['top'][i]),
            "width": int(data['width'][i]),
            "height": int(data['height'][i]),
            "line_num": int(data['line_num'][i]),
            "block_num": int(data['block_num'][i]),
        })

    return words