# Generated by Django 5.1.6 on 2025-02-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_is_special_alter_product_original_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_state',
            field=models.BooleanField(blank=True, default=1, editable=False),
            preserve_default=False,
        ),
    ]
