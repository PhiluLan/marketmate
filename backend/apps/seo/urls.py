# backend/apps/seo/urls.py
from django.urls import path
from apps.seo.views import (
    SEOAuditList,
    TriggerSEOAudit,
    RecommendationView,
    WebsiteSEODetail,
    CrawlWebsiteView,
    SEOAnalyzeAPIView,
)

urlpatterns = [
    # GET  /api/v1/seo/?website_id=…      → List aller Audits (mit Filter)
    path('',                SEOAuditList.as_view(),      name='seo-list-audits'),
    # POST /api/v1/seo/run/               → neuen Audit anstoßen
    path('run/',            TriggerSEOAudit.as_view(),  name='seo-trigger-audit'),
    # GET  /api/v1/seo/recommendations/   → KI-Empfehlungen
    path('recommendations/',RecommendationView.as_view(), name='seo-recommendation'),
    # GET  /api/v1/seo/detail/?website_id=… → Detail-Ansicht einer Website
    path('detail/',         WebsiteSEODetail.as_view(),  name='seo-website-detail'),
    # POST /api/v1/seo/crawl/             → einfacher Crawl-Endpunkt
    path('crawl/',          CrawlWebsiteView.as_view(),  name='seo-crawl'),
    path('seo/analyze/', SEOAnalyzeAPIView.as_view(), name='seo-analyze'),
]
