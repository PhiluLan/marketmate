from rest_framework.viewsets import ModelViewSet
from .models import CalendarEvent
from .serializers import CalendarEventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CalendarEventViewSet(ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
