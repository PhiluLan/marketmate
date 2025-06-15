# backend/keywords/services/serp_service.py

import logging
import time
from urllib.parse import urlparse, parse_qs, unquote
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("keywords.services.serp_service")

# Maximal 20 Ergebnisse pro Aufruf
MAX_RESULTS = 20


def scrape_serp_rankings(domain: str, keywords: list[str], region: str = "CH") -> list[dict]:
    """
    Nutzt Selenium+Headless-Chrome, um für eine fremde Domain
    die Position+URL in den Top-MAX_RESULTS zu finden.
    """
    tld = region.lower() if len(region) == 2 else "com"
    results: list[dict] = []

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--lang=de-DE")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )

    try:
        for term in keywords:
            entry = {"keyword": term, "domain": domain, "position": None, "url": None}
            q = term.replace(" ", "+")
            url = (
                f"https://www.google.{tld}/search"
                f"?q={q}&num={MAX_RESULTS}&hl=de&gl={region.lower()}"
            )

            driver.get(url)
            time.sleep(2)

            # Consent‐Popup wegklicken
            try:
                iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[src*="consent"]')
                driver.switch_to.frame(iframe)
                btn = driver.find_element(
                    By.XPATH,
                    "//button[contains(., 'Ich stimme zu') or contains(., 'Alle akzeptieren') or contains(., 'Accept all')]"
                )
                btn.click()
                driver.switch_to.default_content()
                time.sleep(1)
            except NoSuchElementException:
                pass

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")

            # Links extrahieren
            anchors = soup.select("div.yuRUbf > a")[:MAX_RESULTS]
            if not anchors:
                # Fallback h3→a
                for h3 in soup.select("h3")[:MAX_RESULTS]:
                    a = h3.find_parent("a")
                    if a and a.has_attr("href"):
                        anchors.append(a)

            raw_urls = []
            for idx, a in enumerate(anchors, start=1):
                href = a.get("href", "")
                if href.startswith("/url?"):
                    qs = parse_qs(urlparse(href).query)
                    real = unquote(qs.get("q", [""])[0])
                else:
                    real = href
                raw_urls.append(real)
                if domain.lower() in urlparse(real).netloc.lower():
                    entry["position"] = idx
                    entry["url"] = real
                    break

            logger.debug(f"[SERP] URL: {url}")
            logger.debug(f"[SERP] gefunden: {raw_urls}")
            logger.debug(f"[SERP] Match: pos={entry['position']}, url={entry['url']}")

            results.append(entry)
    finally:
        driver.quit()

    return results


def fetch_serp_results(term: str, num: int = MAX_RESULTS, region: str = "CH") -> list[dict]:
    """
    Nutzt denselben Selenium-Flow, um **alle** Top-Ergebnisse zu extrahieren:
    Titel, URL und Snippet.
    """
    tld = region.lower() if len(region) == 2 else "com"
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--lang=de-DE")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )

    results = []
    try:
        q = term.replace(" ", "+")
        url = (
            f"https://www.google.{tld}/search"
            f"?q={q}&num={num}&hl=de&gl={region.lower()}"
        )
        driver.get(url)
        time.sleep(2)

        # Consent‐Wall
        try:
            iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[src*="consent"]')
            driver.switch_to.frame(iframe)
            btn = driver.find_element(
                By.XPATH,
                "//button[contains(., 'Ich stimme zu') or contains(., 'Alle akzeptieren') or contains(., 'Accept all')]"
            )
            btn.click()
            driver.switch_to.default_content()
            time.sleep(1)
        except NoSuchElementException:
            pass

        soup = BeautifulSoup(driver.page_source, "lxml")
        cards = soup.select("div.g")[:num]

        for card in cards:
            # Google strukturiert sehr unterschiedlich – hier ein Basis-Fallback:
            title_tag = card.select_one("h3")
            link_tag  = card.select_one("div.yuRUbf > a") or card.select_one("a")
            snippet   = card.select_one("div.IsZvec") or card.select_one("span.aCOpRe")

            title = title_tag.get_text(strip=True) if title_tag else ""
            href  = link_tag["href"] if link_tag and link_tag.has_attr("href") else ""
            text  = snippet.get_text(strip=True) if snippet else ""

            results.append({
                "title":   title,
                "url":     href,
                "snippet": text
            })
    finally:
        driver.quit()

    return results
