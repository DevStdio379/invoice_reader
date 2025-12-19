# main.py
import json
import sys
import os
from PIL import Image, ImageDraw, ImageFont
from ocr.loader import load_document
from ocr.preprocess import preprocess
from ocr.ocr_engine import ocr_with_boxes
from parser.header_parser import parse_header
from parser.table_parser import parse_items

def group_words_to_line(words):
    """Group OCR words into ordered lines using block_num + line_num and left coordinate."""
    lines = {}
    for w in words:
        key = (w['block_num'], w['line_num'])
        lines.setdefault(key, []).append(w)

    ordered = []
    for k in sorted(lines.keys()):
        ws = sorted(lines[k], key=lambda x: x['left'])
        text = " ".join([w['text'] for w in ws])
        ordered.append(text)
    return ordered

def process_file(path, include_raw=True):
    """Process a PDF/image invoice and return header, items, and optionally raw OCR words."""
    with open(path, "rb") as f:
        raw = f.read()

    pil = load_document(raw)
    pre = preprocess(pil)
    words = ocr_with_boxes(pre)
    lines = group_words_to_line(words)

    header = parse_header(lines)
    items = parse_items(lines, words)

    result = {
        "header": header,
        "items": items
    }

    if include_raw:
        result["raw_words"] = words

    return result, pil, words  # return image and words for visualization

def draw_ocr_boxes(image: Image.Image, words, output_path="ocr_debug.png"):
    """
    Draw bounding boxes around each OCR word and save the image.
    """
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = None

    for w in words:
        left, top = w['left'], w['top']
        right = left + w['width']
        bottom = top + w['height']
        draw.rectangle([left, top, right, bottom], outline="red", width=2)
        if font:
            draw.text((left, top-10), w['text'], fill="blue", font=font)
        else:
            draw.text((left, top-10), w['text'], fill="blue")

    image.save(output_path)
    print(f"OCR debug image saved as {output_path}")

if __name__ == "__main__":
    sample = "samples/sample-invoice.pdf"
    if len(sys.argv) > 1:
        sample = sys.argv[1]
    if not os.path.exists(sample):
        print("Put an invoice file/image at", sample)
        sys.exit(1)

    # Process invoice
    out, pil_img, words = process_file(sample, include_raw=True)

    # Save JSON output
    with open("invoice_output.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"Processed invoice saved to invoice_output.json")

    # Draw OCR boxes for visual debugging
    draw_ocr_boxes(pil_img, words, output_path="ocr_debug.png")
