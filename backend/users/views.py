from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from apps.seo.models import SEOAudit
import logging

from .serializers import UserSerializer
from apps.seo.tasks import audit_user_website  # Celery-Task

User = get_user_model()
logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'login', 'verify_email']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # 1. Eingabedaten serialisieren und validieren
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Nutzer anlegen (ist in UserManager bereits inactive)
        user = serializer.save()
         # Website sofort zum Profil hinzufügen
        from websites.models import Website
        Website.objects.get_or_create(
        url=user.website_url,
        defaults={'user': user, 'name': user.company_name or '' }
        )

        # 3. Link zur Verifikationsseite erstellen
        verify_url = f"{settings.FRONTEND_URL}/verify-email?token={user.email_verify_token}"

        # 4. E-Mail versenden
        send_mail(
            subject=getattr(settings, 'DEFAULT_FROM_EMAIL_SUBJECT',
                            "Bitte bestätige deine E-Mail"),
            message=(
                "Hallo und willkommen!\n\n"
                "Bitte bestätige deine E-Mail-Adresse, indem du auf den folgenden Link klickst:\n\n"
                f"{verify_url}\n\n"
                "Nach der Bestätigung siehst du direkt deinen personalisierten SEO-Audit."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # 5. SEO-Audit im Hintergrund starten – mit Fallback, falls kein Broker erreichbar
    # Debug-Log vor dem Delay
        logger.info(f"[DEBUG] About to enqueue SEO-Audit task for user {user.id}")
        try:
            result = audit_user_website.delay(user.id)
            logger.info(f"[DEBUG] audit_user_website.delay() returned {result!r}")
        except Exception as e:
            logger.warning(f"[DEBUG] Could not enqueue SEO-Audit task for user {user.id}: {e}")

        # 6. Response zurückgeben
        return Response(
            {"detail": "Registrierung fast abgeschlossen – bitte prüfe dein Postfach."},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            if not user.is_active:
                return Response(
                    {"error": "Account nicht aktiviert. Bitte E-Mail verifizieren."},
                    status=status.HTTP_403_FORBIDDEN
                )
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": self.get_serializer(user).data
            })
        return Response({"error": "Ungültige Zugangsdaten."},
                        status=status.HTTP_401_UNAUTHORIZED)

    @action(
        detail=False,
        methods=['get'],
        url_path='verify-email',
        permission_classes=[permissions.AllowAny]
    )
    def verify_email(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({"detail": "Token fehlt."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email_verify_token=token)
        except User.DoesNotExist:
            return Response({"detail": "Ungültiger Token."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Account aktivieren + Token löschen
        user.is_active = True
        user.email_verify_token = ''
        user.save()

        # Jüngsten SEOAudit holen
        audit = (
            SEOAudit.objects
            .filter(website__url=user.website_url)
            .order_by('-created_at')
            .first()
        )

        # Basis-Metriken zusammenstellen
        metrics = {}
        if audit:
            raw = {
                "score":               audit.score,
                "Ladezeit (ms)":       audit.load_time,
                "Broken Links":        audit.broken_links,
                "Wortanzahl":          audit.word_count,
                "H1-Überschriften":    audit.h1_count,
                "H2-Überschriften":    audit.h2_count,
                "Lesbarkeit (Flesch)": audit.reading_score,
                "Keyword-Dichte (%)":  audit.keyword_density,
            }
            for label, val in raw.items():
                if val is not None:
                    metrics[label] = round(val, 2) if isinstance(val, float) else val

        # sortieren und splitten
        sorted_metrics = sorted(metrics.items(), key=lambda kv: kv[1])
        poor = sorted_metrics[:4]
        top  = sorted_metrics[-4:]
        audit_complete = bool(user.hey_lenny_summary)

        # Social-Media-Daten nur auslesen, wenn audit existiert
        social = {}
        if audit:
            social = {
                "instagram": {
                    "followers":    audit.instagram_followers,
                    "avg_likes":    audit.instagram_avg_likes,
                    "avg_comments": audit.instagram_avg_comments,
                },
                "facebook": {
                    "followers":    audit.facebook_followers,
                    "avg_likes":    audit.facebook_avg_likes,
                    "avg_comments": audit.facebook_avg_comments,
                },
                "linkedin": {
                    "followers":    audit.linkedin_followers,
                    "avg_likes":    audit.linkedin_avg_likes,
                    "avg_comments": audit.linkedin_avg_comments,
                },
            }

        return Response({
            "first_name":        user.first_name,
            "website_url":       user.website_url,
            "hey_lenny_summary": user.hey_lenny_summary or "",
            "audit_complete":    audit_complete,
            "top_metrics":       [{"label": k, "value": v} for k, v in reversed(top)],
            "poor_metrics":      [{"label": k, "value": v} for k, v in poor],
            "social_summary":    social,
        }, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='me',
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(self.get_serializer(request.user).data)


def email_verification_page(request):
    """
    Rendert eine HTML-Seite, die automatisch
    per JavaScript das Audit-Popup öffnet.
    Erwartet den Token in ?token=<...>.
    """
    token = request.GET.get('token', '')
    return render(request, 'users/verify_email.html', {'token': token})
