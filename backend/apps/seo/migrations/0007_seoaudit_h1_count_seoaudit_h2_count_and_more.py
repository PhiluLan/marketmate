# Generated by Django 4.2.21 on 2025-05-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0006_rename_title_seoaudit_meta_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='seoaudit',
            name='h1_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='h2_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='word_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
