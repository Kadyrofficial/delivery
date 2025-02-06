from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class Catalogue(models.Model):
    title_tm = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    parent = models.ForeignKey("self", verbose_name="Parent catalogue", on_delete=models.CASCADE, blank=True, null=True, related_name="subcategories")
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.title_tm
    
    def clean(self):
        if self.parent and self.parent == self:
            raise ValidationError("A category cannot be its own parent.")

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        super().save(*args, **kwargs)
