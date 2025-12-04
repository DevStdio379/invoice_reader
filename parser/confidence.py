# parser/confidence.py

def avg_conf_for_phrase(words, phrase):
    """
    Estimate confidence for a phrase by matching OCR words that appear in the phrase.
    Simple heuristic: split phrase into tokens and average confidences of matching OCR words.
    """

    if not phrase:
        return 0.0
    phrase_tokens = [t.lower() for t in phrase.split() if t.strip()]
    if not phrase_tokens:
        return 0.0
    # map word text -> list of confidences
    word_map = {}
    
    for w in words:
        key = w['text'].lower()
        word_map.setdefault(key, []).append(w['conf'])
    confs = []
    
    for tok in phrase_tokens:
        if tok in word_map:
            confs.append(max(word_map[tok])) # take max confidence for this token

    if not confs:
        # fallback: average all word confidences as weak signal
        return sum(w['conf'] for w in words) / max(1, len(words))
    
    return sum(confs) / len(confs)