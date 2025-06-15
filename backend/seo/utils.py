import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_website(url, max_links=20):
    """
    Crawlt eine Seite einmalig, misst Ladezeit, extrahiert Title, Meta-Desc,
    zählt H1/H2/H3, sucht bis max_links Links und prüft deren Status.
    """
    result = {}
    start = time.time()
    r = requests.get(url, timeout=10)
    load_ms = int((time.time() - start) * 1000)
    result['load_time_ms'] = load_ms

    soup = BeautifulSoup(r.text, 'html.parser')
    result['title_tag'] = (soup.title.string or '').strip()
    meta = soup.find('meta', attrs={'name':'description'})
    result['meta_description'] = (meta.get('content','').strip()
                                  if meta else '')

    # Headings zählen
    for level in (1,2,3):
        result[f'h{level}_count'] = len(soup.find_all(f'h{level}'))

    # Broken Links zählen (einfach per HEAD-Request)
    links = soup.find_all('a', href=True)[:max_links]
    broken = 0
    for a in links:
        href = urljoin(url, a['href'])
        try:
            resp = requests.head(href, timeout=5, allow_redirects=True)
            if resp.status_code >= 400:
                broken += 1
        except requests.RequestException:
            broken += 1
    result['broken_links'] = broken

    # Einfacher Score: 100 minus Summe der fehlenden Basics
    score = 100
    if not result['title_tag']: score -= 20
    if not result['meta_description']: score -= 20
    score -= (result['broken_links'] * 2)
    result['overall_score'] = max(0, score)

    result['raw_data'] = {
        'status_code': r.status_code,
        'headers': dict(r.headers),
    }
    return result
