from django.db import models

class CalendarEvent(models.Model):
    TYPE_CHOICES = [
        ('blog', 'Blog'),
        ('social', 'Social'),
        ('ads', 'Ads'),
    ]

    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title
