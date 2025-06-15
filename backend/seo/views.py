# backend/seo/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import traceback

from seo.models import SEOAudit
from seo.serializers import SEOAuditSerializer
from seo.services.seo_crawler import run_seo_audit
from seo.openai_service import ask_openai
from seo.prompts import meta_description_prompt
from seo.web_crawler import crawl_website

from websites.models import Website
from websites.serializers import WebsiteSerializer

from keywords.services.search_console_service import fetch_rankings_for_domain


class CrawlWebsiteView(APIView):
    """
    POST /api/seo/crawl/
    Body: { "url": "https://www.kuni-gunde.ch" }
    """
    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"error": "URL fehlt"}, status=status.HTTP_400_BAD_REQUEST)
        result = crawl_website(url)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)


class TriggerSEOAudit(APIView):
    """
    POST /api/seo/audit/
    Body: { "website_id": 123 }
    """
    def post(self, request):
        website_id = request.data.get('website_id')
        if not website_id:
            return Response({'detail': 'website_id fehlt'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Website.objects.get(pk=website_id)
        except Website.DoesNotExist:
            return Response({'detail': 'Website nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)

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
    GET  /api/seo/audit/?website_id=<id>
    Liefert alle Audits für eine Website (absteigend nach created_at)
    """
    def get(self, request):
        website_id = request.query_params.get('website_id')
        if not website_id:
            return Response({'detail': 'website_id fehlt'}, status=status.HTTP_400_BAD_REQUEST)

        audits = SEOAudit.objects.filter(website_id=website_id).order_by('-created_at')
        serializer = SEOAuditSerializer(audits, many=True)
        return Response(serializer.data)


class RecommendationView(APIView):
    """
    POST /api/seo/recommendation/
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
        return Response({"recommendation": recommendation})


class WebsiteSEODetail(APIView):
    """
    GET /api/seo/detail/?website_id=<id>
    Liefert:
      - Website-Details
      - Letzte 5 SEO-Audits
      - Google Search Console Daten (Such-Analytics) für die Domain
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        website_id = request.query_params.get('website_id')
        if not website_id:
            return Response({'detail': 'website_id fehlt'}, status=status.HTTP_400_BAD_REQUEST)

        # 1) Website laden und prüfen, ob sie dem aktuellen User gehört
        try:
            website = Website.objects.get(pk=website_id, user=request.user)
        except Website.DoesNotExist:
            return Response(
                {'detail': 'Website nicht gefunden oder kein Zugriff.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2) Letzte 5 Audits holen
        audits = SEOAudit.objects.filter(website=website).order_by('-created_at')[:5]

        # 3) Daten aus der Google Search Console abrufen
        try:
            gsc_data = fetch_rankings_for_domain(website.url)
        except Exception as e:
            return Response(
                {'detail': f'GSC-Fehler: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 4) Alles zusammen in einem JSON zurückgeben
        return Response({
            'website': WebsiteSerializer(website).data,
            'audits': SEOAuditSerializer(audits, many=True).data,
            'search_console': gsc_data,
        }, status=status.HTTP_200_OK)
