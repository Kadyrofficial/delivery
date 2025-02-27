# Generated by Django 5.1.6 on 2025-02-27 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
        ('restaurants', '0005_restaurant_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='banner', to='restaurants.restaurant', verbose_name='Restaurant'),
            preserve_default=False,
        ),
    ]
