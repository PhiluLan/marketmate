# backend/seo/crawler/spiders/audit_spider.py

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from urllib.parse import urlparse, urljoin

def run_audit(url: str) -> dict:
    start = timezone.now()
    resp = requests.get(url, timeout=10)
    load_ms = int((timezone.now() - start).total_seconds() * 1000)
    soup = BeautifulSoup(resp.text, 'html.parser')

    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))

    # Broken Links zählen
    broken = 0
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('http'):
            try:
                r = requests.head(href, timeout=5)
                if r.status_code >= 400:
                    broken += 1
            except requests.RequestException:
                broken += 1

    # SEO Infos extrahieren
    def meta(name):
        tag = soup.find('meta', attrs={'name': name})
        if tag and tag.get('content'):
            return tag['content']
        tag = soup.find('meta', attrs={'property': name})  # og:title etc.
        if tag and tag.get('content'):
            return tag['content']
        return None

    title = soup.title.string if soup.title else None
    meta_description = meta('description')
    meta_robots = meta('robots')
    canonical = None
    link_tag = soup.find('link', rel='canonical')
    if link_tag and link_tag.get('href'):
        canonical = link_tag['href']
    og_title = meta('og:title')
    og_description = meta('og:description')
    h1_count = len(soup.find_all('h1'))
    h2_count = len(soup.find_all('h2'))
    h3_count = len(soup.find_all('h3'))
    h4_count = len(soup.find_all('h4'))
    h5_count = len(soup.find_all('h5'))
    h6_count = len(soup.find_all('h6'))

    word_count = len(soup.get_text().split())
    # === Script-Tags extrahieren ===
    script_urls = []
    for script in soup.find_all('script', src=True):
        src = script['src']
        # ggf. relativen Pfad absolutisieren
        script_urls.append(urljoin(base_url, src))

    # robots.txt prüfen
    robots_url = urljoin(base_url, '/robots.txt')
    try:
        robots_resp = requests.get(robots_url, timeout=5)
        robots_found = robots_resp.status_code == 200
        robots_content = robots_resp.text if robots_found else None
    except Exception:
        robots_found = False
        robots_content = None

    # sitemap.xml prüfen
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    try:
        sitemap_resp = requests.get(sitemap_url, timeout=5)
        sitemap_found = sitemap_resp.status_code == 200
    except Exception:
        sitemap_found = False

    # Gesamt-Textinhalt (für Lesbarkeits- und Keyword-Analyse)
    text_content = soup.get_text(separator=' ')

    return {
        'score': max(0, 100 - broken),
        'load_time': load_ms,
        'broken_links': broken,
        'title': title,
        'meta_description': meta_description,
        'meta_robots': meta_robots,
        'canonical': canonical,
        'og_title': og_title,
        'og_description': og_description,
        'h1_count': h1_count,
        'h2_count': h2_count,
        'h3_count': h3_count,
        'h4_count': h4_count,
        'h5_count': h5_count,
        'h6_count': h6_count,
        'word_count': word_count,
        'http_status': resp.status_code,  # <-- Das ist dein "http_status" Feld!
        'robots_txt_found': robots_found,
        'robots_txt_content': robots_content,
        'sitemap_found': sitemap_found,
        'sitemap_url': sitemap_url if sitemap_found else None,
        'script_urls': script_urls,
        'text_content': text_content,
    }
