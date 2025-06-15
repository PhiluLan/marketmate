from django.conf import settings
from django.db import models
from websites.models import Website


class KeywordMetrics(models.Model):
    keyword = models.CharField(max_length=255, unique=True)
    monthly_searches = models.IntegerField(null=True)
    competition = models.CharField(max_length=10, null=True)
    low_cpc = models.FloatField(null=True)
    high_cpc = models.FloatField(null=True)
    last_updated = models.DateTimeField(auto_now=True)

class Keyword(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='keywords'
    )
    term       = models.CharField(max_length=255)
    region     = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.term} ({self.region})"

class KeywordRanking(models.Model):
    keyword    = models.ForeignKey(
        Keyword,
        on_delete=models.CASCADE,
        related_name='rankings'
    )
    rank       = models.IntegerField()
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']
