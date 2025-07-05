from django.db import models
from django.conf import settings

class MetaIntegration(models.Model):
    user         = models.OneToOneField(
                     settings.AUTH_USER_MODEL,
                     on_delete=models.CASCADE,
                     related_name='meta_integration'
                   )
    access_token = models.TextField()
    account_id   = models.CharField(max_length=64)      # werbekonto
    expires_at   = models.DateTimeField()
    created      = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Meta Ads Integration for {self.user}"
