# Generated by Django 5.1.6 on 2025-04-05 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0003_catalogue_is_popular'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogue',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='catalogue',
            name='image',
        ),
        migrations.RemoveField(
            model_name='catalogue',
            name='original_image',
        ),
        migrations.RemoveField(
            model_name='catalogue',
            name='thumbnail',
        ),
    ]
