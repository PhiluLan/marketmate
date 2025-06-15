from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
# '' sorgt dafür, dass /api/users/ auf die ViewSet-Methoden routed
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
