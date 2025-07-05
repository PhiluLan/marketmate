from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Metric(models.Model):
    METRIC_TYPES = [
        ('organic_sessions', 'Organische Sessions'),
        ('conversions', 'Conversions'),
        ('ad_spend', 'Werbebudget'),
        ('roi', 'Return on Investment'),
        # Du kannst später beliebig ergänzen
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics')
    type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.FloatField()
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'type', 'date')  # pro Tag & Typ nur ein Wert
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} – {self.type} am {self.date}: {self.value}"
    
class CalendarEvent(models.Model):
    CONTENT_TYPES = [
        ('blog', 'Blog'),
        ('social', 'Social'),
        ('ads', 'Ads'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    start = models.DateTimeField()
    end = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.type})"
