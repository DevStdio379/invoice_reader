
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

- Tesseract OCR
- OpenCV
- Pillow
- Python 3.8+
