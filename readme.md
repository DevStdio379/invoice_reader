
# Invoice Reader

A Python application for extracting and parsing invoice data from PDF and image files using OCR.

## Project Structure

```
invoice-reader/
│
├── main.py
├── ocr/
│   ├── loader.py          # Load PDF/image → PIL
│   ├── preprocess.py      # OpenCV preprocessing
│   ├── ocr_engine.py      # Tesseract wrapper
│
├── parser/
│   ├── header_parser.py   # Extract invoice no, date, supplier
│   ├── table_parser.py    # Extract line items
│   ├── confidence.py      # Field confidence scoring
│
└── samples/
    └── invoice1.pdf
```

## Features

- **OCR Pipeline**: Load, preprocess, and extract text from invoices
- **Data Parsing**: Extract header info and line item tables
- **Confidence Scoring**: Validate extraction accuracy

## Dependencies

- python 3.12++ (3.12.7)
- opencv-python
- pillow
- pytesseract
- easyocr
- pandas

## Phase 1 - OCR Layer
- read any invoice image/pdf
- extract text + bounding boxes
- confidence scores for eact text block

## Phase 2 - Invoice Understanding
- detect line items
- detect description, quantity, unit price, total
- confidence scoring per field
- output JSON like:
```
{
  "vendor": "ABC Supplies",
  "date": "2025-02-19",
  "items": [
    {
      "description": "Blue pen",
      "quantity": 24,
      "unit_price": 1.20,
      "confidence": 0.92
    }
  ]
}
```

## [Future] Phase 3 - Inventory Integration
- push extracted items into your system
- check for existing SKU
- log results + uncertainties