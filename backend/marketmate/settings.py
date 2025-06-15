# marketmate/settings.py

from pathlib import Path
import environ

# 1. BASE_DIR definieren
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. .env laden
env = environ.Env()
env.read_env(BASE_DIR / '.env')  # legt fest, wo ENV-Datei liegt

# 3. SECURITY
SECRET_KEY = env('SECRET_KEY', default='django-insecure-…')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = []  # in Prod hier Liste füllen
OPENAI_API_KEY = env('OPENAI_API_KEY')
GOOGLE_API_KEY = env("GOOGLE_API_KEY")
GOOGLE_CSE_ID  = env("GOOGLE_CSE_ID")

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
    'seo',
    'todos',
    'keywords.apps.KeywordsConfig',
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
        'DIRS': [], 
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
