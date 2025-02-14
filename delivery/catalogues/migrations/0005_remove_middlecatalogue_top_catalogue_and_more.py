# Generated by Django 5.1.6 on 2025-02-05 22:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0004_alter_catalogue_slug_alter_middlecatalogue_slug_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='middlecatalogue',
            name='top_catalogue',
        ),
        migrations.RemoveField(
            model_name='catalogue',
            name='middle_catalogue',
        ),
        migrations.AddField(
            model_name='catalogue',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='catalogues.catalogue', verbose_name='Parent catalogue'),
        ),
    ]
