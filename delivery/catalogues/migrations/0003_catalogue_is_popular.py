# Generated by Django 5.1.6 on 2025-02-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0002_catalogue_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogue',
            name='is_popular',
            field=models.BooleanField(default=False),
        ),
    ]
