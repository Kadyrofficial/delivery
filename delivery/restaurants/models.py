from django.db import models
import uuid
from unidecode import unidecode
from django.utils.text import slugify
from locations.models import Location, Address
from django.core.exceptions import ValidationError
from accounts.models import User

def restaurant_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"restaurants/{uuid.uuid4().hex[:12]}.{ext}"

class Restaurant(models.Model):
    title_tm = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    description_tm = models.TextField()
    description_ru = models.TextField()
    image = models.ImageField(upload_to=restaurant_image_upload_path)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    active_status = models.BooleanField(default=False)
    location = models.ForeignKey(Location, verbose_name="Location", on_delete=models.CASCADE, related_name="restaurant_location", blank=True, null=True)
    address = models.ForeignKey(Address, verbose_name="Address", on_delete=models.CASCADE, related_name="restaurant_address", blank=True, null=True)
    user = models.ForeignKey(User, verbose_name="Restaurant User", on_delete=models.CASCADE, related_name="restaurant")
    
    def __str__(self):
        return self.title_tm
    
    def clean(self):
        if self.address.location != self.location:
            raise ValidationError("Selected Address Line does not belong to the selected Etrap City.")

    def save(self, *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        if self.user.is_restaurant_customer == False:
            raise ValidationError("You can choose only Restaurant User")
        super().save(*args, **kwargs)
