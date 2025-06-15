# backend/keywords/views.py

import os
import random

from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .models import Keyword, KeywordRanking, KeywordMetrics
from .serializers import (
    KeywordSerializer,
    KeywordRankingSerializer,
    KeywordMetricsSerializer,
    KeywordIdeaSerializer,
    SERPResultSerializer,
)
from .services.google_ads_service import fetch_keyword_ideas
from .services.search_console_service import fetch_rankings_for_domain
from .services.cse_service import fetch_cse_rankings
from .services.serp_service import scrape_serp_rankings, fetch_serp_results  # neu



class KeywordViewSet(viewsets.ModelViewSet):
    """
    CRUD für Keywords plus Ranking-Check-Action.
    Zugriff nur für authentifizierte User.
    """
    permission_classes = [IsAuthenticated]
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    def get_queryset(self):
        latest = KeywordRanking.objects.order_by('-checked_at')
        return Keyword.objects.filter(user=self.request.user).prefetch_related(
            Prefetch('rankings', queryset=latest, to_attr='latest')
        )

    def perform_create(self, serializer):
        keyword = serializer.save(user=self.request.user)
        manager_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
        if not (manager_id and manager_id.isdigit() and len(manager_id) == 10):
            return
        results = fetch_keyword_ideas([keyword.term], manager_id)
        if results:
            match = next((r for r in results if r["keyword"] == keyword.term), results[0])
            KeywordMetrics.objects.update_or_create(
                keyword=keyword.term,
                defaults={
                    "monthly_searches": match["monthly_searches"],
                    "competition":      match["competition"],
                    "low_cpc":          match["low_cpc"],
                    "high_cpc":         match["high_cpc"],
                }
            )

    @action(detail=True, methods=['post'])
    def check(self, request, pk=None):
        """Simulierter Ranking-Check (Test)"""
        keyword = self.get_object()
        rank = random.randint(1, 100)
        ranking = KeywordRanking.objects.create(keyword=keyword, rank=rank)
        return Response(KeywordRankingSerializer(ranking).data, status=status.HTTP_201_CREATED)



class KeywordMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/keywords/metrics/ liefert alle gespeicherten Keyword-Metriken.
    Zugriff nur für eingeloggte User.
    """
    permission_classes = [IsAuthenticated]
    queryset = KeywordMetrics.objects.order_by('-last_updated')
    serializer_class = KeywordMetricsSerializer



class KeywordIdeaView(APIView):
    """
    GET /api/keywords/ideas/?term=…&region=…
    Öffentliche Keyword-Analyse: Suchvolumen, Wettbewerb, CPC.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        term   = request.query_params.get('term')
        region = request.query_params.get('region', '').lower()
        if not term:
            return Response(
                {'detail': 'Query-Parameter "term" ist erforderlich.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        manager_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
        if not (manager_id and manager_id.isdigit() and len(manager_id) == 10):
            return Response(
                {'detail': 'GOOGLE_ADS_LOGIN_CUSTOMER_ID ist nicht korrekt konfiguriert.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            results = fetch_keyword_ideas([term], manager_id)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not results:
            return Response(status=status.HTTP_204_NO_CONTENT)

        for r in results:
            r['region'] = region

        return Response(results, status=status.HTTP_200_OK)



class KeywordSERPView(APIView):
    """
    GET /api/keywords/serp/?term=…
    Liefert echte Google-SERP-Ergebnisse (Titel, URL, Snippet).
    Öffentlich.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        term = request.query_params.get('term')
        if not term:
            return Response({'error': 'Parameter "term" fehlt.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serp_results = fetch_serp_results(term, num=20)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = SERPResultSerializer(serp_results, many=True)
        return Response({
            'keyword': term,
            'serp':    serializer.data
        }, status=status.HTTP_200_OK)



class KeywordRankingView(APIView):
    """
    GET /api/keywords/rankings/?keywords=kw1,kw2&days_back=7
    Ruft GSC-Daten (eigene Domain) ab.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keywords_param = request.query_params.get('keywords')
        if not keywords_param:
            return Response(
                {"error": "Bitte gib einen 'keywords' Query-Parameter an."},
                status=status.HTTP_400_BAD_REQUEST
            )
        keywords = [kw.strip() for kw in keywords_param.split(',') if kw.strip()]

        days_back = request.query_params.get('days_back')
        try:
            days_back = int(days_back) if days_back is not None else 7
        except ValueError:
            return Response(
                {"error": "Ungültiger 'days_back'-Wert."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            results = fetch_rankings_for_domain(keywords, days_back=days_back)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(results, status=status.HTTP_200_OK)



class CompetitorAnalysisView(APIView):
    """
    GET /api/keywords/competitor/?domain=…&keywords=…&region=…
    Analysiere SERP-Rankings einer fremden Domain via Google CSE.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain   = request.query_params.get('domain')
        keywords = request.query_params.get('keywords', '')
        region   = request.query_params.get('region', 'CH')

        if not domain or not keywords:
            return Response(
                {"error": "Bitte 'domain' und 'keywords' angeben."},
                status=status.HTTP_400_BAD_REQUEST
            )

        kw_list = [k.strip() for k in keywords.split(',') if k.strip()]

        try:
            results = fetch_cse_rankings(domain, kw_list, region)
        except Exception as e:
            return Response(
                {"detail": f"CSE-Fehler: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(results, status=status.HTTP_200_OK)
