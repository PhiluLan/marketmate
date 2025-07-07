# backend/apps/integrations/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    IntegrationViewSet,
    GoogleAuthURLView,
    GoogleCallbackView,
    CampaignsView,
    GoogleAuthURLView,
)

router = DefaultRouter()
router.register(r'', IntegrationViewSet, basename='integration')

urlpatterns = [
    # CRUD-Endpoints für Integrations
    path('', include(router.urls)),

    # Meta-OAuth
    path('meta/connect/',   views.MetaConnectView.as_view(),   name='meta-connect'),
    path('meta/callback/',  views.MetaCallbackView.as_view(),  name='meta-callback'),
    path('meta/overview/',  views.MetaAdsOverview.as_view(),   name='meta-overview'),

    # Google OAuth: erst URL holen, dann Callback
    path('google/auth-url/',  GoogleAuthURLView.as_view(),  name='google-auth-url'),
    path('google/callback/',  GoogleCallbackView.as_view(), name='google-callback'),

    # Campaigns-Listing für jede Integration
    path('<int:pk>/campaigns/', CampaignsView.as_view(), name='integration-campaigns'),
]
