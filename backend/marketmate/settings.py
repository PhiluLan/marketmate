# marketmate/settings.py

import os
from pathlib import Path
import environ
from celery.schedules import crontab
from django.db.backends.signals import connection_created
from django.dispatch import receiver

# 1. BASE_DIR definieren
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. .env laden
env = environ.Env()
env.read_env(BASE_DIR / '.env')  # legt fest, wo ENV-Datei liegt

DATABASES = {
    'default': env.db(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}

# 3. SECURITY
SECRET_KEY = env('SECRET_KEY', default='django-insecure-…')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = []  # in Prod hier Liste füllen
OPENAI_API_KEY = env('OPENAI_API_KEY')
GOOGLE_API_KEY = env("GOOGLE_API_KEY")
GOOGLE_CSE_ID  = env("GOOGLE_CSE_ID")
GOOGLE_OAUTH_CLIENT_ID       = env('GOOGLE_ADS_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET   = env('GOOGLE_ADS_CLIENT_SECRET')
GOOGLE_OAUTH_REDIRECT_URI    = env('GOOGLE_OAUTH_REDIRECT_URI')
GOOGLE_ADS_DEVELOPER_TOKEN   = env('GOOGLE_ADS_DEVELOPER_TOKEN')
GOOGLE_ADS_LOGIN_CUSTOMER_ID = env('GOOGLE_ADS_LOGIN_CUSTOMER_ID', default=None)

ALLOWED_HOSTS = ["*"]

# 4. CORS (Entwicklung)
CORS_ALLOW_ALL_ORIGINS = True
# Oder restriktiv:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     "http://localhost:3000",
# ]
CORS_ALLOW_CREDENTIALS = True

# 5. Apps & Middleware
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'users',
    'websites',
    'apps.seo',
    'todos',
    'keywords.apps.KeywordsConfig',
    'apps.persona_engine',
    'apps.chat',
    'apps.memory_service',
    'apps.rag_service',
    'apps.ads',
    'apps.integrations',
    'django_celery_beat',
    'apps.dashboard',
    'content_calendar',
    'apps.content',
    "apps.distribution",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',    # direkt nach Security
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'marketmate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',  # Optional, falls du beide erlauben willst
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


WSGI_APPLICATION = 'marketmate.wsgi.application'

# 6. Datenbank via django-environ mit Fallback auf SQLite
DATABASES = {
    'default': env.db(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}

# Nur für SQLite: längeres Timeout und Multithread-Zugriff erlauben
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default']['OPTIONS'] = {
        'timeout': 20,            # Warte bis zu 20 Sekunden auf einen Lock
        'check_same_thread': False,
    }

# 7. Auth & weitere Einstellungen
AUTH_USER_MODEL = 'users.User'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "keywords.services.serp_service": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

CELERY_BEAT_SCHEDULE = {
    'fetch_facebook_ads_every_10_seconds': {
        'task': 'apps.ads.tasks.fetch_fb_ads_task',
        'schedule': 10.0,   # alle 10 Sekunden zum Test
        # alternativ: crontab(hour=0, minute=30) für täglich 00:30
    },
}

# ─── Celery Broker & Result Backend ──────────────────────────
# hier die beiden Zeilen hinzufügen:
# ──────────────────────────────────────────────────────────────

# Facebook
FB_APP_ID               = env('APP_ID')
FB_APP_SECRET           = env('APP_SECRET')
META_OAUTH_REDIRECT_URI = env('META_OAUTH_REDIRECT_URI')
FB_SYSTEM_TOKEN        = os.environ['FB_SYSTEM_TOKEN']

# Frontend-URL
FRONTEND_URL                 = os.environ.get("FRONTEND_URL","http://localhost:3001")

# ─── Email-Konfiguration ────────────────────────────────────────
# Email-Konfiguration
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST        = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT        = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER   = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS     = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL  = env('DEFAULT_FROM_EMAIL', default='noreply@deine-domain.de')
DEFAULT_FROM_EMAIL_SUBJECT = env('DEFAULT_FROM_EMAIL_SUBJECT', default='Bitte bestätige deine E-Mail')

DEBUG = True
# ────────────────────────────────────────────────────────────────


# Celery über Redis
CELERY_BROKER_URL     = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')

@receiver(connection_created)
def set_sqlite_pragma(sender, connection, **kwargs):
    engine = connection.settings_dict.get('ENGINE', '')
    if 'sqlite3' in engine:
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA journal_mode=WAL;')