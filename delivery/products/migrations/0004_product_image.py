# Generated by Django 5.1.6 on 2025-02-05 20:01

import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_description_ru_product_description_tm'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=1, upload_to=products.models.product_image_upload_path),
            preserve_default=False,
        ),
    ]
