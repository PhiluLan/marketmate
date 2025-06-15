# backend/keywords/services/cse_service.py

import os
import requests
from django.conf import settings

# Maximal 20 Ergebnisse pro Keyword
MAX_RESULTS = 10

def fetch_cse_rankings(domain: str, keywords: list[str], region: str = "CH") -> list[dict]:
    """
    Nutzt die Custom Search JSON API, um die Top MAX_RESULTS für jedes Keyword
    zu holen und ermittelt Position+URL der angegebenen Domain.
    """
    api_key = settings.GOOGLE_API_KEY
    cse_id  = settings.GOOGLE_CSE_ID

    if not api_key or not cse_id:
        raise RuntimeError("GOOGLE_API_KEY oder GOOGLE_CSE_ID nicht gesetzt")

    base_url = "https://www.googleapis.com/customsearch/v1"
    results = []

    for term in keywords:
        params = {
            "key": api_key,
            "cx":  cse_id,
            "q":   term,
            "num": min(MAX_RESULTS, 10),
            "gl":  region.lower(),
        }
        resp = requests.get(base_url, params=params, timeout=10)
        # Hebt auf 400/403 usw. ab
        resp.raise_for_status()
        data = resp.json()

        # Items = Liste der Treffer
        items = data.get("items", [])
        found_pos = None
        found_url = None

        for idx, item in enumerate(items, start=1):
            link = item.get("link", "")
            if domain.lower() in link.lower():
                found_pos = idx
                found_url = link
                break

        results.append({
            "keyword":  term,
            "domain":   domain,
            "position": found_pos,
            "url":      found_url,
        })

    return results
