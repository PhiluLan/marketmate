from django.apps import AppConfig

class IntegrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # wenn du Django 3.2+ nutzt
    name = 'apps.integrations'                            # <— ganz wichtig!
    verbose_name = "Integrations"
