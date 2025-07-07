from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

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
    
class Integration(models.Model):
    PROVIDER_CHOICES = [
        ("google", "Google Ads"),
        # andere Provider …
    ]
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    provider      = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    access_token  = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at    = models.DateTimeField(blank=True, null=True)
    account_id    = models.CharField(max_length=50, blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "provider")

    def __str__(self):
        return f"{self.user} – {self.get_provider_display()}"
