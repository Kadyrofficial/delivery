from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
from restaurants.models import Restaurant


class Catalogue(models.Model):
    title_tm = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    restaurant = models.ManyToManyField(Restaurant, verbose_name="Restaurants", related_name='catalogues', editable=False)
    is_popular = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title_tm

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        super().save(*args, **kwargs)
