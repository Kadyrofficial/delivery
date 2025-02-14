# Generated by Django 5.1.6 on 2025-02-06 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_address_line_user_city_province_user_etrap_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='CustomerUser',
            fields=[
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='DeliveryManUser',
            fields=[
            ],
            options={
                'verbose_name': 'Delivery Man',
                'verbose_name_plural': 'Delivery Men',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='RestaurantCustomerUser',
            fields=[
            ],
            options={
                'verbose_name': 'Restaurant Customer',
                'verbose_name_plural': 'Restaurant Customers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_delivery_man',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_restaurant_customer',
            field=models.BooleanField(default=False),
        ),
    ]
