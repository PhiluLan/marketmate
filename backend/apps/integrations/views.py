# apps/integrations/views.py

import os, requests, datetime
from django.shortcuts import redirect as django_redirect
from django.utils import timezone
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import MetaIntegration

class MetaConnectView(View):
    def get(self, request):
        client_id    = settings.FB_APP_ID
        redirect_uri = settings.META_OAUTH_REDIRECT_URI
        scope        = 'ads_read,ads_management'
        oauth_url    = (
            f"https://www.facebook.com/v17.0/dialog/oauth"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
        )
        return django_redirect(oauth_url)

class MetaCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        client_id     = settings.FB_APP_ID
        client_secret = settings.FB_APP_SECRET
        redirect_uri  = settings.META_OAUTH_REDIRECT_URI

        token_res = requests.get(
            "https://graph.facebook.com/v17.0/oauth/access_token",
            params={
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "client_secret": client_secret,
                "code": code,
            }
        ).json()
        token   = token_res['access_token']
        expires = timezone.now() + datetime.timedelta(seconds=token_res.get('expires_in',0))

        acct_res = requests.get(
            "https://graph.facebook.com/v17.0/me/adaccounts",
            params={"access_token": token, "fields":"account_id"}
        ).json()
        account_id = acct_res['data'][0]['account_id']

        mi, _ = MetaIntegration.objects.update_or_create(
            user=request.user,
            defaults={
              "access_token": token,
              "expires_at": expires,
              "account_id": account_id
            }
        )
        return django_redirect(settings.FRONTEND_URL + "/integrations")

class MetaAdsOverview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        mi = request.user.meta_integration
        res = requests.get(
          f"https://graph.facebook.com/v17.0/act_{mi.account_id}/ads",
          params={
            "access_token": mi.access_token,
            "fields": "id,name,insights.limit(1){impressions,clicks,spend}",
            "limit": 50
          }
        )
        return Response(res.json())
