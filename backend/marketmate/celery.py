# backend/marketmate/celery.py
import os
from celery import Celery

# 1. Django Settings-Modul setzen
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmate.settings')

# 2. Celery-App initialisieren und Broker direkt übergeben
app = Celery(
    'marketmate',
    broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
)

# 3. Konfiguration aus Django-Settings parsen (namespace CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Tasks in allen INSTALLED_APPS automatisch finden
app.autodiscover_tasks()
