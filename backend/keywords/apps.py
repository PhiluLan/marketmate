from django.apps import AppConfig
from django.db import connections


class KeywordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keywords'

    def ready(self):
        conn = connections['default']
        engine = conn.settings_dict.get('ENGINE', '')
        # nur bei SQLite das WAL-Pragma setzen
        if 'sqlite3' in engine:
            with conn.cursor() as cursor:
                cursor.execute('PRAGMA journal_mode=WAL;')
