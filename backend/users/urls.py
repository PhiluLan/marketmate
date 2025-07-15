from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, email_verification_page

# Router für User-Endpoints: Registrierung, Login, Verify-Email, Me
router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    # /api/users/              -> POST Registrierung (create)
    # /api/users/login/        -> POST Login
    # /api/users/verify-email/ -> GET E-Mail-Verifikation + SEO-Audit
    # /api/users/me/           -> GET Benutzerprofil
    path('', include(router.urls)),
    path('verify-email-page/', email_verification_page, name='verify-email-page'),
]
