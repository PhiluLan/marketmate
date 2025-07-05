# backend/apps/seo/tasks.py

from celery import shared_task

# für einfachen Text-Crawl
from apps.seo.web_crawler import crawl_website

# für kompletten SEO-Audit
from apps.seo.services.seo_crawler import run_seo_audit

# Pinecone-Client
from services.vector_store import VectorStore

# für Deep-Research via Scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from apps.seo.crawler.spiders.deep_spider import DeepSpider
from celery import shared_task


@shared_task
def task_deep_crawl(url: str) -> dict:
    """
    Blitz-Crawl nur mit BeautifulSoup → Titel, Meta, H1/H2, Wortzahl.
    Eignet sich für RAG-Booster.
    """
    result = crawl_website(url)
    if result.get("success"):
        text = "\n\n".join((
            result.get("title", ""),
            result.get("meta_description", ""),
            f"H1s: {result['h1_count']}, H2s: {result['h2_count']}, Wörter: {result['word_count']}"
        ))
        VectorStore.upsert([{"id": f"deep:{url}", "text": text}])
    return result


@shared_task
def task_deep_crawl_and_index(url: str):
    """
    Crawl die Seite, indexiere Title, Meta-Description UND den Fließtext.
    """
    result = crawl_website(url)
    if result.get("error"):
        return {"error": result["error"]}

    docs = []
    prefix = url.rstrip("/").replace("://", "_")

    # 1) Haupttext (begrenze auf z.B. 10.000 Zeichen, um zu große Embeddings zu vermeiden)
    text = result.get("text_content", "")
    if text:
        snippet = text[:10000]
        docs.append({
            "id": f"{prefix}_text",
            "text": snippet
        })

    # 2) Titel & Meta-Description
    for field in ("title", "meta_description"):
        if val := result.get(field):
            docs.append({
                "id": f"{prefix}_{field}",
                "text": f"{field.replace('_', ' ').title()}: {val}"
            })

    # 3) Upsert in VectorStore
    VectorStore.upsert(docs)
    return {"indexed": len(docs)}


@shared_task
def task_deep_research(url: str) -> dict:
    """
    Vollständiger Deep-Spider über Scrapy, indexiert alle gefundenen Items per PineconePipeline.
    """
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    deferred = runner.crawl(DeepSpider, url=url)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()
    return {"status": "completed", "url": url}


@shared_task
def task_seo_audit(site_id: int) -> dict:
    """
    Führt den umfangreichen SEO-Audit durch und speichert das Ergebnis in der DB.
    """
    audit = run_seo_audit(site_id)
    return {"audit_id": audit.id, "website": audit.website.url}
