# backend/keywords/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    KeywordViewSet,
    KeywordMetricsViewSet,
    KeywordIdeaView,
    KeywordRankingView,
    CompetitorAnalysisView,
    KeywordSERPView,
)

router = DefaultRouter()
router.register('keywords', KeywordViewSet, basename='keyword')
router.register('metrics', KeywordMetricsViewSet, basename='keyword-metrics')

urlpatterns = [
    path('', include(router.urls)),
    path('ideas/', KeywordIdeaView.as_view(), name='keyword-ideas'),
    path('rankings/', KeywordRankingView.as_view(),  name='keyword-rankings'),
    path('competitor/', CompetitorAnalysisView.as_view(), name='competitor-analysis'),
    path('serp/', KeywordSERPView.as_view(), name='keyword-serp'),
]
