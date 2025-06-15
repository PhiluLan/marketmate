from django.apps import AppConfig
from django.db import connections


class KeywordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keywords'

    def ready(self):
        conn = connections['default']
        with conn.cursor() as cursor:
            cursor.execute('PRAGMA journal_mode=WAL;')
