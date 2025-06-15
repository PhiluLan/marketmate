from django.urls import path
from .views import SEOAuditList, TriggerSEOAudit
from .views import SEOAuditList, TriggerSEOAudit, RecommendationView
from .views import WebsiteSEODetail
from .views import CrawlWebsiteView

urlpatterns = [
    # GET  /api/seo/audit/?website_id=…
    path('', SEOAuditList.as_view(), name='seo-list-audits'),

    # POST /api/seo/audit/run/   → Audit starten
    path('run/', TriggerSEOAudit.as_view(), name='seo-trigger-audit'),

    path('', SEOAuditList.as_view(), name='seo-list-audits'),
    path('run/', TriggerSEOAudit.as_view(), name='seo-trigger-audit'),
    # NEU: KI-Empfehlungen
    path('recommendations/', RecommendationView.as_view(), name='seo-recommendation'),
    path('detail/', WebsiteSEODetail.as_view(), name='seo-website-detail'),
    path('crawl/', CrawlWebsiteView.as_view(), name='seo-crawl'),
]
