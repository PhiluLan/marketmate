# apps/seo/views.py

import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.seo.models import SEOAudit
from apps.seo.serializers import (
    SEOAuditSerializer,
    SEOAnalyzeSerializer,
)
from apps.seo.services.seo_crawler import run_seo_audit
from apps.seo.services.seo_client import analyze_seo
from apps.seo.openai_service import ask_openai
from apps.seo.prompts import meta_description_prompt

from websites.models import Website
from websites.serializers import WebsiteSerializer

from keywords.services.search_console_service import fetch_rankings_for_domain


class CrawlWebsiteView(APIView):
    """
    POST /api/v1/seo/crawl/
    Body: { "url": "https://example.com" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"error": "URL fehlt"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = crawl_website(url)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(result, status=status.HTTP_200_OK)


class TriggerSEOAudit(APIView):
    """
    POST /api/v1/seo/audit/
    Body: { "website_id": 123 }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        website_id = request.data.get('website_id')
        if not website_id:
            return Response(
                {'detail': 'website_id fehlt'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Website.objects.get(pk=website_id, user=request.user)
        except Website.DoesNotExist:
            return Response(
                {'detail': 'Website nicht gefunden oder kein Zugriff.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            audit = run_seo_audit(int(website_id))
        except Exception as e:
            tb = traceback.format_exc()
            return Response(
                {'detail': 'Audit fehlgeschlagen', 'error': str(e), 'traceback': tb},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = SEOAuditSerializer(audit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SEOAuditList(APIView):
    """
    GET /api/v1/seo/audit/?website_id=<id>
    Liefert alle Audits für eine Website (absteigend nach created_at)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        website_id = request.query_params.get('website_id')
        if not website_id:
            return Response(
                {'detail': 'website_id fehlt'},
                status=status.HTTP_400_BAD_REQUEST
            )

        audits = SEOAudit.objects.filter(website_id=website_id).order_by('-created_at')
        serializer = SEOAuditSerializer(audits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecommendationView(APIView):
    """
    POST /api/v1/seo/recommendation/
    Body: { "website_name": "...", "website_topic": "..." }
    KI-gestützte Meta-Description-Empfehlung via OpenAI.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        website_name = request.data.get("website_name")
        website_topic = request.data.get("website_topic")
        if not website_name or not website_topic:
            return Response(
                {"error": "website_name und website_topic sind erforderlich."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        prompt = meta_description_prompt(website_name, website_topic)
        recommendation = ask_openai(prompt)
        return Response({"recommendation": recommendation}, status=status.HTTP_200_OK)


class WebsiteSEODetail(APIView):
    """
    GET /api/v1/seo/detail/?website_id=<id>
    Liefert:
      - Website-Details
      - Letzte 5 SEO-Audits
      - Google Search Console Daten für die Domain
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        website_id = request.query_params.get('website_id')
        if not website_id:
            return Response(
                {'detail': 'website_id fehlt'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            website = Website.objects.get(pk=website_id, user=request.user)
        except Website.DoesNotExist:
            return Response(
                {'detail': 'Website nicht gefunden oder kein Zugriff.'},
                status=status.HTTP_404_NOT_FOUND
            )

        audits = SEOAudit.objects.filter(website=website).order_by('-created_at')[:5]

        try:
            gsc_data = fetch_rankings_for_domain(website.url)
        except Exception as e:
            return Response(
                {'detail': f'GSC-Fehler: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'website': WebsiteSerializer(website).data,
            'audits': SEOAuditSerializer(audits, many=True).data,
            'search_console': gsc_data,
        }, status=status.HTTP_200_OK)


class SEOAnalyzeAPIView(APIView):
    """
    POST /api/v1/seo/analyze/
    Body: { "text": "...", "keyword": "optional" }
    Returns: { flesch_score, keyword_density, meta_advice }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SEOAnalyzeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = analyze_seo(
            text=data['text'],
            keyword=data.get('keyword', '')
        )
        return Response(result, status=status.HTTP_200_OK)
