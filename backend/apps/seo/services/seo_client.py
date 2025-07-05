# apps/seo/services/seo_client.py
import re
from textstat import flesch_reading_ease

def keyword_density(text: str, keyword: str) -> float:
    """
    Gibt die Dichte in Prozent zurück. Bei leerem Keyword immer 0.0.
    """
    if not keyword:
        return 0.0

    # Zähle exakte Vorkommen des Keywords (Wortgrenzen!)
    count = len(re.findall(rf'\b{re.escape(keyword)}\b', text, flags=re.IGNORECASE))
    # Zähle alle Wörter im Text
    total_words = len(re.findall(r'\b\w+\b', text))

    if total_words == 0:
        return 0.0

    density = (count / total_words) * 100
    return round(density, 2)

def analyze_seo(text: str, keyword: str = '') -> dict:
    flesch = flesch_reading_ease(text)
    density = keyword_density(text, keyword)
    meta_advice = 'Meta-Description fehlt' if len(text) < 150 else 'Meta-Länge OK'
    return {
        'flesch_score': round(flesch, 2),
        'keyword_density': density,
        'meta_advice': meta_advice
    }
