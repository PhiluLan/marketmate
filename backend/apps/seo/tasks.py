# backend/apps/seo/tasks.py

from celery import shared_task
from django.apps import apps
import logging

# für OpenAI-basierten SEO-Audit
from .openai_service import audit_website

# für einfachen Text-Crawl
from apps.seo.web_crawler import crawl_website

# für kompletten SEO-Audit mit crawler
from apps.seo.services.seo_crawler import run_seo_audit

# Pinecone-Client
from services.vector_store import VectorStore

# für Deep-Research via Scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from apps.seo.crawler.spiders.deep_spider import DeepSpider

logger = logging.getLogger(__name__)

task_deep_crawl_doc = """
Blitz-Crawl nur mit BeautifulSoup → Titel, Meta, H1/H2, Wortzahl.
Eignet sich für RAG-Booster.
"""

@shared_task
def audit_user_website(user_id: int) -> dict:
    User    = apps.get_model('users', 'User')
    Website = apps.get_model('websites', 'Website')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning(f"User {user_id} nicht gefunden, skipping audit")
        return {"user_id": user_id, "error": "User not found"}

    # heyLenny-Summary über OpenAI
    from .openai_service import audit_website
    summary = audit_website(user.website_url, user.first_name)
    user.hey_lenny_summary = summary
    user.save()

    # Website-Objekt erstellen/holen
    website_obj, _ = Website.objects.get_or_create(
        url=user.website_url,
        defaults={'user': user}
    )

    # SEO-Audit-Task für Metriken
    from .tasks import task_seo_audit
    task_seo_audit.delay(website_obj.id)

    # ────────── Social-Media-Metriken ──────────
    from apps.seo.services.social_metrics import (
        fetch_instagram_metrics,
        fetch_facebook_metrics,
        fetch_linkedin_metrics,
    )

    sm_inst = fetch_instagram_metrics(user.instagram_url) if user.instagram_url else {}
    sm_fb   = fetch_facebook_metrics(user.facebook_url)   if user.facebook_url   else {}
    sm_li   = fetch_linkedin_metrics(user.linkedin_url)   if user.linkedin_url   else {}

    # In den letzten SEOAudit-Datensatz speichern
    audit = (
        apps.get_model('seo', 'SEOAudit').objects
        .filter(website=website_obj)
        .order_by('-created_at')
        .first()
    )
    if audit:
        audit.instagram_followers    = sm_inst.get('followers')
        audit.instagram_avg_likes    = sm_inst.get('avg_likes')
        audit.instagram_avg_comments = sm_inst.get('avg_comments')

        audit.facebook_followers     = sm_fb.get('followers')
        audit.facebook_avg_likes     = sm_fb.get('avg_likes')
        audit.facebook_avg_comments  = sm_fb.get('avg_comments')

        audit.linkedin_followers     = sm_li.get('followers')
        audit.linkedin_avg_likes     = sm_li.get('avg_likes')
        audit.linkedin_avg_comments  = sm_li.get('avg_comments')

        audit.save()
    # ────────────────────────────────────────────

    logger.info(f"Audit und Social-Media-Metrics für User {user.id} abgeschlossen")
    return {"user_id": user.id, "summary_length": len(summary)}

@shared_task
def task_deep_crawl(url: str) -> dict:
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

    text = result.get("text_content", "")
    if text:
        snippet = text[:10000]
        docs.append({"id": f"{prefix}_text", "text": snippet})

    for field in ("title", "meta_description"):
        if val := result.get(field):
            docs.append({"id": f"{prefix}_{field}", "text": f"{field.replace('_', ' ').title()}: {val}"})

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

