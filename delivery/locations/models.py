from django.db import models
from unidecode import unidecode
from django.utils.text import slugify


class Location(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    queue = models.PositiveIntegerField(unique=True)
    
    def __str__(self):
        return self.title_tm

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        super().save(*args, **kwargs)


class Address(models.Model):
    title = models.CharField(max_length=100)
    location = models.ForeignKey(Location, verbose_name="Location", on_delete=models.CASCADE, related_name="location")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title))
        super().save(*args, **kwargs)
