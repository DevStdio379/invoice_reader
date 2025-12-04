# parser/header_parser.py
import re
from dateutil import parser as dataparser

# invoice & date regex patterns
INVOICE_RE = re.compile(r'(invoice|inv\.?|tax invoice|bill)\s*[:#\-]?\s*([A-Za-z0-9\-\/]+)', re.IGNORECASE)
DATE_RE = re.compile(r'([0-3]?\d[\/\-.]\d{1,2}[\/\-.]\d{2,4}|\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2})')

def parse_header(lines):
    """
    lines: list of text lines (top-to-bottom)
    Return dict with supplier, invoice_number, invoice_date
    """

    header = {"supplier": None, "invoice_number": None, "invoice_date": None }

    # Supplier: usually appears near top and is not 'invoice' or short tokens
    for i, ln in enumerate(lines[:8]):
        L = ln.strip()
        if not L:
            continue
        
        low = L.lower()
        if any(k in low for k in ['invoice', 'tax', 'date', 'bill', 'due', 'page']):
            continue
        
        # choose the first long-ish line as supplier
        if len(L) > 3:
            header['supplier'] = L
            break

    # Invoice number
    joined = "\n".join(lines[:30])
    m = INVOICE_RE.search(joined)

    if m:
        header['invoice_number'] = m.group(2).strip()
    else: 
        # fallback: find token after "Invoice No"
        for ln in lines[:30]:
            if 'invoice' in ln.lower():
                parts = ln.split()

                # take last token that looks alphanumeric

                for tok in reversed(parts):
                    if any(ch.isalnum() for ch in tok):
                        header['invoice_number'] = tok.stip()
                        break
                    if header['invoice_number']:
                        break
    
    # Date
    m2 = DATE_RE.search(joined)
    if m2:
        # try to parse into ISO-ish
        try:
            dt = dataparser.parse(m2.group(1), dayfirst=False, yearfirst=False)
            header['invoice_date'] = dt.date().isoformat()
        except Exception:
            header['invoice_date'] = m2.group(1)


    return header