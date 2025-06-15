# keywords/tasks.py
from celery import shared_task
from .services.google_ads_service import fetch_keyword_ideas
from .models import KeywordMetrics

@shared_task
def update_keyword_metrics(keywords, customer_id):
    data = fetch_keyword_ideas(keywords, customer_id)
    for item in data:
        KeywordMetrics.objects.update_or_create(
            keyword=item["keyword"],
            defaults={
                "monthly_searches": item["monthly_searches"],
                "competition": item["competition"],
                "low_cpc": item["low_cpc"],
                "high_cpc": item["high_cpc"],
            }
        )
