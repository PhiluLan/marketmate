# Generated by Django 4.2.21 on 2025-06-01 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0023_seoaudit_domain_authority_seoaudit_trust_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='seoaudit',
            name='anchor_text_distribution',
            field=models.TextField(blank=True, help_text='JSON-Array der Top-Ankertexte mit Häufigkeiten', null=True),
        ),
    ]
