def detect_table_columns(words):
    """
    Detect table header row and approximate column positions.
    Returns a dict: column_name -> left x-coordinate
    """

    # keywords to detect columns
    keywords = ['item','description','qty','uom','unit','price','discount','total']

    # add common OCR misreads
    ocr_fixes = {
        'Itam': 'item',
        'description': 'description',
        'qut': 'qty'
    }

    # group words by line (top coordinate)
    lines = {}

    # grouping word into rows
    for w in words:
        top_key = w['top'] // 5 # integer division to group nearby tops
        lines.setdefault(top_key, []).append(w)

    print(f'lines: {len(lines)}')


    # find the line that contains most column keywords
    best_line = None
    best_count = 0

    for line_words in lines.values():
        text_line = " ".join([w['text'].lower() for w in line_words])
        count = sum(1 for kw in keywords if kw in text_line)
        if count > best_count:
            best_count = count
            best_line = line_words

    if not best_line:
        return None # could not detect header
    
    # assign left positions to keywords
    columns = {}

    for w in best_line:
        word_text = w['text'].lower()
        # apply fix
        word_text = ocr_fixes.get(word_text, word_text)

        # only register first match
        if word_text in keywords and word_text not in columns:
            columns[word_text] = w['left']

    return columns