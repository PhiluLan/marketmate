from django.db import models


class Content(models.Model):
    # Basis-Felder
    title = models.CharField(max_length=200, help_text="Überschrift / Name des Contents")
    body = models.TextField(blank=True, help_text="Text oder Beschreibung")
    image = models.ImageField(upload_to="content_images/", blank=True, null=True)

    # Ads-Parameter (optional bei organischen Posts)
    ad_account_id    = models.CharField(max_length=50, blank=True, null=True, help_text="Meta Ad Account ID")
    objective        = models.CharField(max_length=50, blank=True, null=True, help_text="Ad-Objective, z.B. LINK_CLICKS")
    daily_budget     = models.PositiveIntegerField(blank=True, null=True, help_text="Budget pro Tag in Cent")
    spend_cap        = models.PositiveIntegerField(blank=True, null=True, help_text="Max. Gesamtausgaben in Cent")
    start_time       = models.DateTimeField(blank=True, null=True, help_text="Anzeigen-Startzeit (Ads)")
    end_time         = models.DateTimeField(blank=True, null=True, help_text="Anzeigen-Endzeit (Ads)")
    attribution_spec = models.JSONField(blank=True, null=True, help_text="Attribution-Spezifikation als JSON-Liste")

    def __str__(self):
        return self.title
