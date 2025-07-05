from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services.facebook_ads_service import create_meta_ad_campaign

class CreateFacebookCampaignView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            campaign = create_meta_ad_campaign(**request.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        return Response(campaign)
