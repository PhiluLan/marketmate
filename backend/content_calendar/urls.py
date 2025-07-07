from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CalendarEventViewSet

router = DefaultRouter()
# List, Create    → GET/POST  /api/scheduler/
# Retrieve, Update, Delete → /api/scheduler/{pk}/
router.register(r'scheduler', CalendarEventViewSet, basename='scheduler')

urlpatterns = [
    path('', include(router.urls)),
]