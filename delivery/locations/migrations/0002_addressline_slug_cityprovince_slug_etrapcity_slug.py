# Generated by Django 5.1.6 on 2025-02-06 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressline',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='cityprovince',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='etrapcity',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
    ]
