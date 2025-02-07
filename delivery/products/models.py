from decimal import Decimal
from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify
from unidecode import unidecode
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from catalogues.models import Catalogue
from restaurants.models import Restaurant


def product_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"products/{uuid.uuid4().hex[:12]}.{ext}"


class ActiveProduct(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_status=True, restaurant__active_status=True)

class Product(models.Model):
    title_tm = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    description_tm = models.TextField()
    description_ru = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=0, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, blank=True)
    image = models.ImageField(upload_to=product_image_upload_path)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    catalogue = models.ForeignKey(Catalogue, verbose_name="Catalogue of the Product", on_delete=models.CASCADE, related_name="product")
    restaurant = models.ForeignKey(Restaurant, verbose_name="Restaurant of the Product", on_delete=models.CASCADE, related_name="product")
    active_status = models.BooleanField(default=True)
    objects = models.Manager() 
    active_products = ActiveProduct()

    def __str__(self):
        return self.title_tm

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        self.price = self.initial_price * (Decimal('1') - self.discount / Decimal('100'))
        super().save(*args, **kwargs)
