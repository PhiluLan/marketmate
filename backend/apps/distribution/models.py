from django.db import models
from apps.content.models import Content

class ScheduledPost(models.Model):
    CHANNEL_CHOICES = [
        ("facebook",      "Facebook (organisch)"),
        ("instagram",     "Instagram (organisch)"),
        ("facebook_ads",  "Facebook Ads"),
        ("email",         "E-Mail"),
    ]
    STATUS_CHOICES = [
        ("pending", "Ausstehend"),
        ("sent",    "Gesendet"),
        ("failed",  "Fehlgeschlagen"),
    ]

    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES,
        help_text="Ziel-Channel, z.B. facebook_ads"
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        help_text="Verknüpft das Content-Objekt"
    )
    scheduled_time = models.DateTimeField(
        help_text="Datum & Uhrzeit der Ausspielung"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        help_text="Status: pending, sent oder failed"
    )

    def __str__(self):
        return f"{self.channel} @ {self.scheduled_time} ({self.status})"
