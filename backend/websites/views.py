from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Website
from .serializers import WebsiteSerializer

class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Website.objects.none()  # Leeres QuerySet statt 500-Fehler!
        return Website.objects.filter(user=user)

    def perform_create(self, serializer):
        # die neue Website automatisch dem aktuellen User zuweisen
        serializer.save(user=self.request.user)
