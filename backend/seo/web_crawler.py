# backend/seo/web_crawler.py

import requests
from bs4 import BeautifulSoup
import scrapy

def crawl_website(url):
    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
    except Exception as e:
        return {"error": f"Fehler beim Abrufen der Seite: {str(e)}"}

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extrahiere die wichtigsten Infos:
    title = soup.title.string.strip() if soup.title else ""
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    # Statistiken
    h1_count = len(soup.find_all("h1"))
    h2_count = len(soup.find_all("h2"))
    text = soup.get_text(separator=" ", strip=True)
    word_count = len(text.split())

    return {
        "title": title,
        "meta_description": meta_desc,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "word_count": word_count,
        "success": True,
    }

class SeoSpider(scrapy.Spider):
    name = "seo"
    custom_settings = {"DOWNLOAD_TIMEOUT": 20}

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        def get_meta(name):
            return response.xpath(
                f'//meta[@name="{name}"]/@content | //meta[@property="{name}"]/@content'
            ).get()
        def get_link(rel):
            return response.xpath(f'//link[@rel="{rel}"]/@href').get()

        yield {
            "url": response.url,
            "title": response.xpath('//title/text()').get(),
            "meta_description": get_meta("description"),
            "meta_robots": get_meta("robots"),
            "meta_hreflang": response.xpath('//link[@rel="alternate"]/@hreflang').getall(),
            "canonical": get_link("canonical"),
            "og_title": get_meta("og:title"),
            "og_description": get_meta("og:description"),
            "twitter_card": get_meta("twitter:card"),
            "twitter_description": get_meta("twitter:description"),
            # Du kannst hier beliebig viele weitere Felder ergänzen!
        }
