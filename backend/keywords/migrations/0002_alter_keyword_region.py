# Generated by Django 4.2.21 on 2025-05-23 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keywords', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='region',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
