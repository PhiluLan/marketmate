import os
import requests
import ssl
import socket
import urllib.robotparser
import xml.etree.ElementTree as ET
import json
from django.utils import timezone
from seo.crawler.spiders.audit_spider import run_audit
from seo.models import SEOAudit
from websites.models import Website


# --------------------------------------------------------
# Hilfsfunktion: Normalisiert Website-URL (stellt sicher, dass "https://" vorangestellt ist)
# --------------------------------------------------------
def normalize_url(u: str) -> str:
    if u.startswith("http://") or u.startswith("https://"):
        return u.rstrip("/")  # nur ganz sicher den abschließenden "/" entfernen
    return "https://" + u.rstrip("/")


# --------------------------------------------------------
# Hauptfunktion: Führt das gesamte SEO-Audit durch
# --------------------------------------------------------
def run_seo_audit(website_id: int) -> SEOAudit:
    # 1) Website-Objekt aus der DB holen
    website = Website.objects.get(pk=website_id)
    # 2) Normalisierte URL (immer mit https://)
    norm_url = normalize_url(website.url)

    # --------------------------------------------------------
    # 1) Redirect-Analyse: Kettenlänge & Schleifen erkennen
    # --------------------------------------------------------
    redirect_chain_length = None
    redirect_loop = False
    try:
        resp0 = requests.get(
            norm_url,
            timeout=(5, 30),
            allow_redirects=True
        )
        history = getattr(resp0, 'history', [])
        redirect_chain_length = len(history)
        seen = set()
        for r in history:
            loc = r.headers.get('Location') or r.url
            if loc in seen:
                redirect_loop = True
                break
            seen.add(loc)
    except Exception:
        # Beim Fehlschlag ignorieren wir (redirect_chain_length bleibt None)
        pass

    # --------------------------------------------------------
    # 2) SSL-Zertifikat & Security-Header (HSTS, CSP)
    # --------------------------------------------------------
    ssl_valid_until = None
    cipher_strength = None
    hsts = False
    csp = False
    try:
        # a) SSL-/Zertifikat-Daten
        hostname = norm_url.split("://")[1].split("/")[0]
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, 443))
            cert = s.getpeercert()
            not_after = cert.get('notAfter')
            # Beispiel-Format: 'Aug 29 04:23:41 2025 GMT'
            ssl_valid_until = timezone.datetime.strptime(
                not_after, '%b %d %H:%M:%S %Y %Z'
            )
            # Cipher-Stärke (z.B. 'AES256-SHA')
            cipher_strength = s.cipher()[1]

        # b) Security-Header per HEAD-Request checken
        head = requests.head(norm_url, timeout=5)
        hsts = 'strict-transport-security' in head.headers
        csp = 'content-security-policy'     in head.headers
    except Exception:
        # Wenn irgendetwas schiefgeht, lassen wir die Felder bei None/False
        pass

    # --------------------------------------------------------
    # 3) HTML-Crawling: run_audit liefert Grunddaten (Title, Meta, H1/H2, Broken Links, etc.)
    # --------------------------------------------------------
    result = run_audit(norm_url)

    # a) JS-Rendering: Sollten Skript-URLs vorliegen, speichern wir sie als JSON-String
    scripts = result.get('script_urls', [])
    js_render_blocking_resources = None
    if scripts:
        js_render_blocking_resources = json.dumps(scripts, ensure_ascii=False, indent=2)

    # b) robots.txt-Direktiven auslesen
    robots_directives = None
    try:
        rp = urllib.robotparser.RobotFileParser()
        robots_url = result.get('robots_txt_url') or f"{norm_url.rstrip('/')}/robots.txt"
        rp.set_url(robots_url)
        rp.read()
        # Für Debug/Visualisierung speichern wir den kompletten Inhalt der robots.txt
        raw = requests.get(robots_url, timeout=5).text
        robots_directives = raw
    except Exception:
        robots_directives = None

    # c) Sitemap-Validität prüfen
    sitemap_valid = False
    sitemap_errors = None
    try:
        sitemap_url = result.get('sitemap_url') or f"{norm_url.rstrip('/')}/sitemap.xml"
        resp_sm = requests.get(sitemap_url, timeout=5)
        resp_sm.raise_for_status()
        ET.fromstring(resp_sm.text)  # Parst das XML
        sitemap_valid = True
    except Exception as e:
        sitemap_valid = False
        sitemap_errors = str(e)

    # d) Basis-Metriken aus dem Crawler-Ergebnis
    score = result.get('score', 100)
    load_time = result.get('load_time', 0)
    broken_links = result.get('broken_links', 0)
    h1_count = result.get('h1_count', 0)
    h2_count = result.get('h2_count', 0)
    h3_count = result.get('h3_count', 0)
    h4_count = result.get('h4_count', 0)
    h5_count = result.get('h5_count', 0)
    h6_count = result.get('h6_count', 0)
    word_count = result.get('word_count', 0)

    # --------------------------------------------------------
    # 4) Title-Tag-Check (Länge + Keyword-Position)
    # --------------------------------------------------------
    title = result.get('title') or ''
    title_length = len(title)
    title_keyword_position = None
    try:
        from keywords.models import Keyword
        primary = Keyword.objects.filter(website=website).order_by('-created_at').first()
        if primary:
            kw = getattr(primary, 'keyword', None) or getattr(primary, 'name', '')
            idx = title.lower().find(kw.lower()) if kw else -1
            title_keyword_position = (idx + 1) if idx >= 0 else 0
    except Exception:
        title_keyword_position = None

    # --------------------------------------------------------
    # 5) Meta-Description-Check (Länge + Einzigartigkeit)
    # --------------------------------------------------------
    meta_desc = result.get('meta_description') or ''
    meta_description_length = len(meta_desc)
    meta_description_unique = True
    try:
        previous = SEOAudit.objects.filter(website=website).order_by('-created_at')[:5]
        for prev in previous:
            if prev.meta_description == meta_desc and prev.meta_description:
                meta_description_unique = False
                break
    except Exception:
        meta_description_unique = True

    # --------------------------------------------------------
    # 6) PageSpeed Insights (Core Web Vitals: FCP, LCP, CLS, TTI)
    # --------------------------------------------------------
    fcp = lcp = cls = tti = None
    try:
        api_key = os.getenv("PAGESPEED_API_KEY")
        psi_url = (
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
            f"?url={norm_url}&key={api_key}"
            "&category=performance"
            "&strategy=mobile"
        )
        resp_psi = requests.get(psi_url, timeout=(5, 30)).json()
        audits = resp_psi["lighthouseResult"]["audits"]
        fcp = audits["first-contentful-paint"]["numericValue"]
        lcp = audits["largest-contentful-paint"]["numericValue"]
        cls = audits["cumulative-layout-shift"]["numericValue"]
        tti = audits["interactive"]["numericValue"]
    except Exception:
        # Wenn PSI fehlschlägt, ignorieren wir (Felder bleiben None)
        pass

    # --------------------------------------------------------
    # 7) Off-Page: Backlinks, Referring Domains, DA & Trust Score via Moz URL Metrics
    # --------------------------------------------------------
    backlink_count = None
    referring_domains = None
    domain_authority = None
    trust_score = None
    try:
        token = os.getenv("MOZ_API_TOKEN")
        moz_endpoint = "https://lsapi.seomoz.com/v2/url_metrics/"
        payload = {
            "targets": [norm_url],
            "metrics": [
                "external_pages_to_root_domain",
                "root_domains_to_root_domain",
                "domain_authority",
                "spam_score"
            ]
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        resp_moz = requests.post(
            moz_endpoint, headers=headers, json=payload, timeout=10
        )
        if resp_moz.status_code == 200:
            data_moz = resp_moz.json().get("results", [{}])[0]
            backlink_count = data_moz.get("external_pages_to_root_domain")
            referring_domains = data_moz.get("root_domains_to_root_domain")
            domain_authority = data_moz.get("domain_authority")
            trust_score = data_moz.get("spam_score")
        else:
            # Wenn Status != 200, belassen wir es bei None
            pass
    except Exception:
        backlink_count = None
        referring_domains = None
        domain_authority = None
        trust_score = None

    # --------------------------------------------------------
    # 8) Off-Page: Ankertext-Verteilung via Moz Anchor Text Endpoint
    # --------------------------------------------------------
    anchor_text_distribution = None
    try:
        token = os.getenv("MOZ_API_TOKEN")
        moz_endpoint_anchors = "https://lsapi.seomoz.com/v2/anchor_text"
        payload_anchors = {
            "target": norm_url,
            "limit": 5
        }
        headers_anchors = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        resp_anchors = requests.post(
            moz_endpoint_anchors,
            headers=headers_anchors,
            json=payload_anchors,
            timeout=10
        )
        if resp_anchors.status_code == 200:
            raw_results = resp_anchors.json().get("results", [])
            if raw_results:
                anchor_text_distribution = json.dumps(
                    raw_results, ensure_ascii=False, indent=2
                )
            else:
                anchor_text_distribution = None
        else:
            # Kein 200 → nichts speichern
            pass
    except Exception:
        anchor_text_distribution = None

    # --------------------------------------------------------
    # 9) Content-Lesbarkeit & Keyword-Dichte (Flesch, etc.)
    # --------------------------------------------------------
    reading_score = None
    keyword_density = None
    try:
        text = result.get('text_content', '') or ''
        words = [w for w in text.split() if w.isalpha()]
        total_words = len(words)
        total_sentences = max(1, text.count('.') + text.count('!') + text.count('?'))
        total_syllables = sum(count_syllables(w) for w in words)
        reading_score = (
            206.835
            - 1.015 * (total_words / total_sentences)
            - 84.6  * (total_syllables / total_words)
        )
        primary = None
        from keywords.models import Keyword
        primary = Keyword.objects.filter(website=website).order_by('-created_at').first()
        if primary and getattr(primary, 'keyword', None):
            kw = primary.keyword.lower()
        elif primary and getattr(primary, 'name', None):
            kw = primary.name.lower()
        else:
            kw = ''
        if kw and total_words > 0:
            count_kw = sum(1 for w in words if w.lower() == kw)
            keyword_density = (count_kw / total_words) * 100
        else:
            keyword_density = 0.0
    except Exception:
        reading_score = None
        keyword_density = None

    # --------------------------------------------------------
    # 10) Duplicate-Content-Erkennung (Intra-Site)
    # --------------------------------------------------------
    duplicate_sections = None
    try:
        text = result.get('text_content', '') or ''
        import re
        sentences = re.split(r'(?<=[\.\!\?])\s+', text)
        counts = {}
        for s in sentences:
            s_clean = s.strip()
            if len(s_clean) < 20:
                continue
            counts[s_clean] = counts.get(s_clean, 0) + 1
        duplicates = [s for s, c in counts.items() if c > 1]
        if duplicates:
            duplicate_sections = json.dumps(duplicates, ensure_ascii=False, indent=2)
        else:
            duplicate_sections = None
    except Exception:
        duplicate_sections = None

    # --------------------------------------------------------
    # 11) Alles in der DB speichern
    # --------------------------------------------------------
    audit = SEOAudit.objects.create(
        website=website,
        score=score,
        load_time=load_time,
        broken_links=broken_links,
        meta_title=result.get('title'),
        meta_description=result.get('meta_description'),
        meta_robots=result.get('meta_robots'),
        canonical=result.get('canonical'),
        og_title=result.get('og_title'),
        og_description=result.get('og_description'),
        h1_count=h1_count,
        h2_count=h2_count,
        h3_count=h3_count,
        h4_count=h4_count,
        h5_count=h5_count,
        h6_count=h6_count,
        word_count=word_count,
        http_status=result.get('http_status'),
        robots_txt_found=result.get('robots_txt_found', False),
        robots_txt_content=result.get('robots_txt_content'),
        sitemap_found=result.get('sitemap_found', False),
        sitemap_url=result.get('sitemap_url'),

        # Core Web Vitals
        fcp=fcp,
        lcp=lcp,
        cls=cls,
        tti=tti,

        # Redirect-Analyse
        redirect_chain_length=redirect_chain_length,
        redirect_loop=redirect_loop,

        # SSL & Security Header
        ssl_valid_until=ssl_valid_until,
        cipher_strength=cipher_strength,
        hsts=hsts,
        csp=csp,

        # robots.txt & Sitemap
        robots_directives=robots_directives,
        sitemap_valid=sitemap_valid,
        sitemap_errors=sitemap_errors,

        js_render_blocking_resources=js_render_blocking_resources,

        # Title-Tag-Check
        title_length=title_length,
        title_keyword_position=title_keyword_position,

        # Meta-Description-Check
        meta_description_length=meta_description_length,
        meta_description_unique=meta_description_unique,

        # Content-Lesbarkeit & Keyword-Dichte
        reading_score=reading_score,
        keyword_density=keyword_density,

        # Duplicate-Content-Erkennung
        duplicate_sections=duplicate_sections,

        # Off-Page (Moz URL Metrics)
        backlink_count=backlink_count,
        referring_domains=referring_domains,
        domain_authority=domain_authority,
        trust_score=trust_score,

        # Off-Page (Moz Anchor Text)
        anchor_text_distribution=anchor_text_distribution,
    )

    return audit
