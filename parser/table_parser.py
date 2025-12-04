# parser/table_parser.py
import re
from .confidence import avg_conf_for_phrase

AMOUNT_RE = re.compile(r'\d{1,3}(?:[,\s]\d{3})*(?:[.,]\d{2})|\d+\.\d+|\d+')

def find_table_start(lines):
    keywords = ['description', 'item', 'quantity', 'price', 'amount', 'total', 'unit']

    for idx, ln in enumerate(lines):
        low = ln.lower()
        if any(k in low for k in keywords):
            return idx
        
    # fallback: return first line that containes two numbers (qty + price)
    for idx, ln in enumerate(lines):
        nums = AMOUNT_RE.findall(ln)
        if len(nums) >= 2:
            return idx
    
    return None

def parse_items(lines, words):
    """
    Simple heuristic table parser.
    - Find probable table start.
    - For following lines until a blank or footer, extract description (left segment)
      and numbers (qty / unit / total) by finding numeric tokens.
    - Return list of {description, qty, unit_price, line_total, confidence}
    """

    start = find_table_start(lines) or 0
    items = []

    for ln in lines[start + 1 : start + 1 + 80]: # parse up to 80 lines after header
        if not ln.strip():
            # stop on empty line heuristically (end of table)
            break
        nums = AMOUNT_RE.findall(ln)
        if not nums:
            # might still be a long description line - try continue
            continue

        # description: text before first numeric occurrence
        split_by_num = re.split(r'\d', ln, maxsplit=1)
        description = split_by_num[0].strip() if split_by_num else ln.strip()

        # heuristics to assign numbers: qty likely integer and near start; total likely rightmost
        qty = None
        unit_pice = None
        line_total = None

        # clean numeric tokens (remove spaces in thousands)
        cleaned = [n.replace(' ', '').replace(',','') for n in nums]

        if len(cleaned) == 1:
            line_total = cleaned[0]
        elif len(cleaned) == 2:
            # guess qty + price or price + total; try integer for qty
            if cleaned[0].isdigit():
                qty = int(cleaned[0])
                unit_price = cleaned[1]
            else:
                unit_price = cleaned[0]
                line_total = cleaned[1]
        else: 
            # 3+ numbers: (qty, unit, total) or (unit, qty, total)
            # choose last as total
            line = cleaned[-1]
            # choose first integer-ish as qty
            for c in cleaned[:-1]:
                if c.isdigit():
                    qty = int(c)
                    break
            # choose a candidate for unit_price
            for c in cleaned[:-1]:
                if c != str(qty):
                    unit_price = c
                    break
    
        # confidence estimation
        desc_conf = avg_conf_for_phrase(words, description)
        qty_conf = 1.0 if qty is not None else 0.0
        
        if qty is not None:
            # get average confidence of tokens matching qty if any
            qty_conf = avg_conf_for_phrase(words, str(qty))
        unit_conf = avg_conf_for_phrase(words, str(unit_price)) if unit_price else 0.0
        total_conf = avg_conf_for_phrase(words, str(line_total)) if line_total else 0.0
        
        items.append({
            "description": description,
            "qty": qty,
            "unit_price": unit_price,
            "line_total": line_total,
            "confidence": {
                "description": round(desc_conf, 3),
                "qty": round(qty_conf, 3),
                "unit_price": round(unit_conf, 3),
                "line_total": round(total_conf, 3)
            }
        })
    return items