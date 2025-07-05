import os
import sys
import django
import random
from datetime import date, timedelta

# Setze Django-Umgebung

# Füge das "backend/"-Verzeichnis zum Python-Pfad hinzu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketmate.settings')
django.setup()

from apps.dashboard.models import Metric
from django.contrib.auth import get_user_model

User = get_user_model()

# 👤 Benutzer holen (du kannst auch user_id direkt setzen)
users = User.objects.all()

start_date = date.today() - timedelta(days=29)

metric_types = {
    'organic_sessions': (800, 2500),
    'conversions':      (5, 50),
    'ad_spend':         (10, 200)
}

created = 0

for user in users:
    print(f"➕ Erzeuge Daten für: {user.email if user.email else user.username}")

    for i in range(30):
        day = start_date + timedelta(days=i)

        for metric_type, (low, high) in metric_types.items():
            value = random.uniform(low, high)

            obj, is_created = Metric.objects.get_or_create(
                user=user,
                type=metric_type,
                date=day,
                defaults={'value': round(value, 2)}
            )
            if is_created:
                created += 1

print(f"✅ {created} neue Metrics für {users.count()} Nutzer angelegt.")
