# Generated by Django 4.2.21 on 2025-06-13 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('keywords', '0003_keywordmetrics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='website',
        ),
        migrations.AddField(
            model_name='keyword',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='keywords', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
