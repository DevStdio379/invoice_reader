# main.py
import json
from ocr.loader import load_document
from ocr.preprocess import preprocess
from ocr.ocr_engine import ocr_with_boxes
from parser.header_parser import parse_header
from parser.table_parser import parse_items

def group_words_to_line(words):
    """
    Group OCR words into ordered lines using block num + line_num and left coordinate.
    Return list of line text top-to-bottom.
    """
    lines = {}

    for w in words:
        key = (w['block_num'], w['line_num'])
        lines.setdefault(key, []).append(w)

    # sort by block, line then by left
    ordered = []

    for k in sorted(lines.keys()):
        ws = sorted(lines[k], key = lambda x: x['left'])
        text = " ".join([w['text'] for w in ws])
        ordered.append(text)

    return ordered

def process_file(path):
    with open(path, "rb") as f:
        raw = f.read()

    pil = load_document(raw)
    pre = preprocess(pil)
    words = ocr_with_boxes(pre)
    lines = group_words_to_line(words)

    header = parse_header(lines)
    items = parse_items(lines, words)

    return{ "header": header, "items": items}

if __name__ == "__main__":
    import sys, os

    sample = "sample-invoice.pdf"

    if len(sys.argv) > 1:
        sample = sys.argv[1]
    if not os.path.exists(sample):
        print("Put an invoice file/image at", sample)
        sys.exit(1)

    out = process_file(sample)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    