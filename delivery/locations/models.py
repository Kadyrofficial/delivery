from django.db import models


class CityProvince(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title_tm


class EtrapCity(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    city_province = models.ForeignKey(CityProvince, verbose_name="CityProvince", on_delete=models.CASCADE, related_name="city_province")
    
    def __str__(self):
        return self.title_tm


class AddressLine(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    etrap_city = models.ForeignKey(EtrapCity, verbose_name="EtrapCity", on_delete=models.CASCADE, related_name="etrap_city")

    def __str__(self):
        return self.title_tm
