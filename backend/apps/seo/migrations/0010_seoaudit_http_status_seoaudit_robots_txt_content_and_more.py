# Generated by Django 4.2.21 on 2025-05-29 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0009_alter_seoaudit_meta_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seoaudit',
            name='http_status',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='robots_txt_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='robots_txt_found',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='sitemap_found',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='sitemap_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
