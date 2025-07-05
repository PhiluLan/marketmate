from rest_framework import viewsets
from .models import ScheduledPost
from .serializers import ScheduledPostSerializer

class ScheduledPostViewSet(viewsets.ModelViewSet):
    queryset = ScheduledPost.objects.all().order_by("-scheduled_time")
    serializer_class = ScheduledPostSerializer
