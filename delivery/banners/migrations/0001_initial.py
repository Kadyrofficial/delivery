# Generated by Django 5.1.6 on 2025-02-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='')),
                ('image', models.ImageField(blank=True, editable=False, null=True, upload_to='')),
                ('original_image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
