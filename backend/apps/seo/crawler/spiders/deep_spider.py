# apps/seo/crawler/spiders/deep_spider.py
import scrapy
from urllib.parse import urlparse, urljoin

class DeepSpider(scrapy.Spider):
    name = "deep_spider"
    custom_settings = {
        "DOWNLOAD_TIMEOUT": 15,
        "ITEM_PIPELINES": {
            "apps.seo.crawler.pipelines.PineconePipeline": 300,
        }
    }

    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]

    def parse(self, response):
        # Basis-Daten yielden
        yield {
            "url": response.url,
            "title": response.xpath("//title/text()").get(default="").strip(),
            "meta_description": response.xpath(
                "//meta[@name='description']/@content | //meta[@property='og:description']/@content"
            ).get(default="").strip(),
        }
        # alle internen Links weiter crawlen
        for href in response.xpath("//a/@href").getall():
            if href.startswith("/") or self.allowed_domains[0] in href:
                yield response.follow(href, self.parse)
