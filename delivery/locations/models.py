from django.db import models
from unidecode import unidecode
from django.utils.text import slugify


class CityProvince(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.title_tm
    
    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        super().save(*args, **kwargs)


class EtrapCity(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    city_province = models.ForeignKey(CityProvince, verbose_name="CityProvince", on_delete=models.CASCADE, related_name="etrap_city")
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.title_tm

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        super().save(*args, **kwargs)


class AddressLine(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    etrap_city = models.ForeignKey(EtrapCity, verbose_name="EtrapCity", on_delete=models.CASCADE, related_name="address_line")
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.title_tm

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        super().save(*args, **kwargs)
