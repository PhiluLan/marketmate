# Generated by Django 4.2.21 on 2025-06-29 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('type', models.CharField(choices=[('blog', 'Blog'), ('social', 'Social'), ('ads', 'Ads')], max_length=20)),
            ],
        ),
    ]
