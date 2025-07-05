import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ContentGenerateSerializer,
    AssetGenerateSerializer,
)
from .services.openai_client import generate_content
from .services.image_client import generate_image
from rest_framework import viewsets
from .models import Content
from .serializers import ContentSerializer

logger = logging.getLogger(__name__)

class ContentGenerateAPIView(APIView):
    def post(self, request):
        serializer = ContentGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        text = generate_content(
            format_type=data['type'],
            tone=data['tone'],
            length=data['length'],
            topic=data['topic']
        )
        return Response({'content': text}, status=status.HTTP_200_OK)
    
class AssetGenerateAPIView(APIView):
    """
    POST /api/v1/assets/generate/
    Body: {
      "prompt": "Text-Beschreibung",
      "n": 1,               # Anzahl der Bilder (1–4)
      "size": "512x512"     # Auflösung
    }
    Response: { images: [url1, url2, ...] }
    """
    def post(self, request):
        # 1) Validierung des Requests
        serializer = AssetGenerateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # 2) Versuch, das Bild zu generieren
        try:
            urls = generate_image(
                prompt=data['prompt'],
                n=data['n'],
                size=data['size']
            )
        except Exception as e:
            # Logge die volle Exception-Info für Debugging
            logger.error("Bildgenerierung fehlgeschlagen", exc_info=True)
            return Response(
                {"detail": "Bildgenerierung fehlgeschlagen", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 3) Erfolg: Liste der Bild-URLs zurückgeben
        return Response({"images": urls}, status=status.HTTP_200_OK)

class ContentViewSet(viewsets.ModelViewSet):
    """
    Vollständiges CRUD für Content-Objekte.
    """
    queryset = Content.objects.all().order_by("-id")
    serializer_class = ContentSerializer
