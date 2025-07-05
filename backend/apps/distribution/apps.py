from django.apps import AppConfig

class DistributionConfig(AppConfig):
    name = "apps.distribution"
    def ready(self):
        import apps.distribution.signals
