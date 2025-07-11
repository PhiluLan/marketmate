# Generated by Django 4.2.21 on 2025-05-27 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0004_seoaudit_canonical_seoaudit_h1_count_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seoaudit',
            name='h1_count',
        ),
        migrations.RemoveField(
            model_name='seoaudit',
            name='h2_count',
        ),
        migrations.RemoveField(
            model_name='seoaudit',
            name='meta_title',
        ),
        migrations.RemoveField(
            model_name='seoaudit',
            name='word_count',
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='meta_hreflang',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='twitter_card',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='seoaudit',
            name='twitter_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='broken_links',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='canonical',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='load_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='meta_description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='meta_robots',
            field=models.CharField(blank=True, default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='og_description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='og_title',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seoaudit',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
