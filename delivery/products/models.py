from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

class Product(models.Model):
    title_tm = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.title_tm
    
    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        super().save(*args, **kwargs)
