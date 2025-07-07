# backend/apps/integrations/views.py

import requests
import json
import base64

from django.conf import settings
from django.shortcuts import redirect as django_redirect, get_object_or_404
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from google_auth_oauthlib.flow import Flow
from google.ads.googleads.client import GoogleAdsClient

from .models import MetaIntegration, Integration
from .serializers import IntegrationSerializer, MetaIntegrationSerializer
from .services.google_ads_service import list_accessible_customers, list_campaigns
from .services.meta_service import list_meta_campaigns


class MetaConnectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        oauth_url = (
            f"https://www.facebook.com/v17.0/dialog/oauth"
            f"?client_id={settings.FB_APP_ID}"
            f"&redirect_uri={settings.META_OAUTH_REDIRECT_URI}"
            f"&scope=ads_read,ads_management"
        )
        return django_redirect(oauth_url)


class MetaCallbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({"detail": "Missing code parameter."}, status=400)

        token_res = requests.get(
            "https://graph.facebook.com/v17.0/oauth/access_token",
            params={
                "client_id":     settings.FB_APP_ID,
                "redirect_uri":  settings.META_OAUTH_REDIRECT_URI,
                "client_secret": settings.FB_APP_SECRET,
                "code":          code,
            }
        ).json()
        token   = token_res.get('access_token')
        expires = timezone.now() + datetime.timedelta(seconds=token_res.get('expires_in', 0))

        acct_res = requests.get(
            "https://graph.facebook.com/v17.0/me/adaccounts",
            params={"access_token": token, "fields": "account_id"}
        ).json()
        account_id = acct_res.get('data', [{}])[0].get('account_id')

        MetaIntegration.objects.update_or_create(
            user=request.user,
            defaults={
                "access_token": token,
                "expires_at":   expires,
                "account_id":   account_id,
            }
        )

        return django_redirect(settings.FRONTEND_URL + "/integrations")


class MetaAdsOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mi = get_object_or_404(MetaIntegration, user=request.user)
        res = requests.get(
            f"https://graph.facebook.com/v17.0/act_{mi.account_id}/ads",
            params={
                "access_token": mi.access_token,
                "fields":       "id,name,insights.limit(1){impressions,clicks,spend}",
                "limit":        50,
            }
        )
        return Response(res.json())


class GoogleAuthURLView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # JWT aus Header
        auth_header = request.headers.get("Authorization", "")
        jwt_token = auth_header.split(" ",1)[1] if auth_header.startswith("Bearer ") else None

        # state = base64(JSON({jwt:…}))
        state = base64.urlsafe_b64encode(json.dumps({"jwt": jwt_token}).encode()).decode()

        flow = Flow.from_client_config({
                "web": {
                    "client_id":     settings.GOOGLE_OAUTH_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                    "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
                    "token_uri":     "https://oauth2.googleapis.com/token",
                }
            },
            scopes=["https://www.googleapis.com/auth/adwords"],
            redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
            state=state
        )
        print("AUTH_URL:", auth_url)
        return Response({"auth_url": auth_url})


# ganz oben in views.py importieren
import traceback

class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 0) state und code abfragen
        raw_state = request.GET.get("state", "")
        code      = request.GET.get("code", "")
        if not raw_state or not code:
            return Response({"detail": "Missing state or code"}, status=400)

        # 1) JWT aus state lesen und User authentifizieren
        try:
            decoded = base64.urlsafe_b64decode(raw_state.encode()).decode()
            payload = json.loads(decoded)
            jwt_token = payload.get("jwt")
            validated = JWTAuthentication().get_validated_token(jwt_token)
            user = JWTAuthentication().get_user(validated)
        except Exception as e:
            print("⚠️ JWT-Parsing Error:", e)
            return Response({"detail": "Invalid state/token"}, status=400)

        # 2) OAuth Token-Exchange
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id":     settings.GOOGLE_OAUTH_CLIENT_ID,
                        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                        "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
                        "token_uri":     "https://oauth2.googleapis.com/token",
                    }
                },
                scopes=["https://www.googleapis.com/auth/adwords"],
                state=raw_state,
                redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI
            )
            flow.fetch_token(code=code)
            creds = flow.credentials
        except Exception as e:
            print("⚠️ Token-Exchange Error:", e)
            return Response({"detail": "OAuth token exchange failed"}, status=400)

        # 3) expiry timezone-aware machen
        expiry = creds.expiry  # naive datetime
        if expiry is not None and expiry.tzinfo is None:
            expiry = timezone.make_aware(expiry, timezone.utc)

        # 4) Integration speichern
        integ, _ = Integration.objects.update_or_create(
            user=user,
            provider="google",
            defaults={
                "access_token":  creds.token,
                "refresh_token": creds.refresh_token,
                "expires_at":    expiry,
            }
        )

        # 5) Tatsächliche Kunden-IDs holen und erstes Nicht-MCC-Konto auswählen
        try:
            customer_ids = list_accessible_customers(integ.refresh_token)
            # erstes Konto ungleich Demo/MCC
            actual = next(
                (cid for cid in customer_ids
                 if cid != settings.GOOGLE_ADS_LOGIN_CUSTOMER_ID),
                None
            )
            integ.account_id = actual or (customer_ids[0] if customer_ids else "")
        except Exception as e:
            print("⚠️ list_accessible_customers Error:", e)
            # Fallback: demo/MCC-Konto
            integ.account_id = settings.GOOGLE_ADS_LOGIN_CUSTOMER_ID

        integ.save()

        # 6) Zurück ins Frontend
        return django_redirect(settings.FRONTEND_URL + "/integrations/google")



class IntegrationViewSet(viewsets.ModelViewSet):
    serializer_class   = IntegrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return Integration.objects.filter(user=self.request.user)
        except Exception as e:
            print("⚠️ Error in get_queryset:", e)
            return Integration.objects.none()

    @action(detail=True, methods=['get'])
    def campaigns(self, request, pk=None):
        print(f"🛠️ IntegrationViewSet.campaigns called for user={request.user} integration_id={pk}")
        integration = self.get_object()
        try:
            if integration.provider == "google":
                data = list_campaigns(request.user)
            else:
                data = []
        except Exception as e:
            print("⚠️ Error in IntegrationViewSet.campaigns:", e)
            data = []
        print("🛠️ IntegrationViewSet.campaigns returning data:", data)
        return Response(data)


class CampaignsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        print(f"🛠️ CampaignsView GET called for user={request.user} integration_id={pk}")
        integ = Integration.objects.filter(pk=pk, user=request.user).first()
        if not integ:
            print("🛠️ CampaignsView: no integration found, returning []")
            return Response([], status=200)

        try:
            if integ.provider == "google":
                data = list_campaigns(request.user)
            else:
                data = []
        except Exception as e:
            print("⚠️ Error in CampaignsView:", e)
            data = []

        print("🛠️ CampaignsView returning data:", data)
        return Response(data, status=200)