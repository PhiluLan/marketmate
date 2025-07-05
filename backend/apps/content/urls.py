from django.urls import path
from .views import ContentGenerateAPIView
from .views import AssetGenerateAPIView
from rest_framework.routers import DefaultRouter
from .views import ContentViewSet

urlpatterns = [
    path('content/generate/', ContentGenerateAPIView.as_view(), name='content-generate'),
    path('assets/generate/', AssetGenerateAPIView.as_view(), name='assets-generate'),
]

router = DefaultRouter()
router.register(r'contents', ContentViewSet, basename='content')

# die URL-Muster der ViewSet-Router anhängen
urlpatterns += router.urls
