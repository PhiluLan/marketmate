"""
URL configuration for marketmate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', lambda req: JsonResponse({'status': 'ok'})),
    path('api/health/', lambda req: JsonResponse({'status': 'ok'})),
    # JWT-Token-Endpoints
    path('api/token/',       TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/',    include('users.urls')),
    path('api/websites/', include('websites.urls')),
    path('api/keywords/', include('keywords.urls')),
    path('api/seo/',      include('apps.seo.urls')),
    path('api/todos/',    include('todos.urls')),
    path('api/',               include('apps.content.urls')),
    path('api/',          include('content_calendar.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
]
