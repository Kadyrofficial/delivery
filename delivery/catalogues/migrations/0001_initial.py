# Generated by Django 5.1.6 on 2025-02-15 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_tm', models.CharField(max_length=150)),
                ('title_ru', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
                ('thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='')),
                ('image', models.ImageField(blank=True, editable=False, null=True, upload_to='')),
                ('original_image', models.ImageField(upload_to='')),
                ('date_added', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
        ),
    ]
