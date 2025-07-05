from django.urls import path
from .views import CreateFacebookCampaignView

urlpatterns = [
    path('facebook/create_campaign/', CreateFacebookCampaignView.as_view(), name='fb-create-campaign'),
]
