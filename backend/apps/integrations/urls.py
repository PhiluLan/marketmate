from django.urls import path
from . import views

urlpatterns = [
  path('meta/connect/',  views.MetaConnectView.as_view(),  name='meta-connect'),
  path('meta/callback/', views.MetaCallbackView.as_view(), name='meta-callback'),
  path('meta/overview/', views.MetaAdsOverview.as_view(),  name='meta-overview'),
]
