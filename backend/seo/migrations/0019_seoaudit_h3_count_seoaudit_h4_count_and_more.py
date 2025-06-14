# Generated by Django 4.2.21 on 2025-05-31 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0018_seoaudit_meta_description_length_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seoaudit',
            name='h3_count',
            field=models.IntegerField(blank=True, help_text='Anzahl der <h3>-Überschriften', null=True),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='h4_count',
            field=models.IntegerField(blank=True, help_text='Anzahl der <h4>-Überschriften', null=True),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='h5_count',
            field=models.IntegerField(blank=True, help_text='Anzahl der <h5>-Überschriften', null=True),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='h6_count',
            field=models.IntegerField(blank=True, help_text='Anzahl der <h6>-Überschriften', null=True),
        ),
    ]
