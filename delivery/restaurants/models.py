from django.db import models
import os
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.utils import timezone
from locations.models import Location, Address
from django.core.exceptions import ValidationError


class Restaurant(models.Model):
    title_tm = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    thumbnail = models.ImageField(null=True, blank=True, editable=False)
    image = models.ImageField(null=True, blank=True, editable=False)
    original_image = models.ImageField(blank=True)
    date_added = models.DateTimeField(blank=True, null=True, editable=False)
    phone_number = models.CharField(max_length=15)
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    location = models.ForeignKey(Location, verbose_name="Location", on_delete=models.CASCADE, related_name="restaurant_location")
    address = models.ForeignKey(Address, verbose_name="Address", on_delete=models.CASCADE, related_name="restaurant_address")
    user = models.ForeignKey('accounts.User', verbose_name="User", on_delete=models.CASCADE, related_name="restaurant")
    is_active = models.BooleanField()
    is_online = models.BooleanField()
    is_top = models.BooleanField()
    is_delivery_free =  models.BooleanField()
    is_new = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title_tm
    
    def clean(self):
        if self.address.location != self.location:
            raise ValidationError("Selected Address Line does not belong to the selected Etrap City.")
        if self.user.type != self.user.UserType.CLIENT:
            raise ValidationError("The user must be Client")
        
    def save(self, lg=1000, sm=400, originals='restaurants/', images='restaurants/images/', thumbnails='restaurants/thumbnails/', *args, **kwargs):
        
        self.slug = unidecode(slugify(self.title_tm))
        if not self.pk:
            self.date_added = timezone.now()

        if self.original_image:
            if not os.path.exists(self.original_image.path):
                try:
                    old_instance = Restaurant.objects.get(pk=self.pk)
                    os.remove(old_instance.image.path)
                    os.remove(old_instance.thumbnail.path)
                except:
                    print('The Products old image does not exist')
            self.original_image.name = originals + str(slugify(self.date_added)) + '.webp'
            super().save(*args, **kwargs)
            img_instance = Image.open(self.original_image.path)
            aspect_ratio = img_instance.height / img_instance.width
            if img_instance.height > img_instance.width:
                target_height = int(aspect_ratio * lg)
                target_height_thumb = int(aspect_ratio * sm)
                img = img_instance.resize((lg, target_height), Image.Resampling.LANCZOS)
                thmb = img_instance.resize((sm, target_height_thumb), Image.Resampling.LANCZOS)
            elif img_instance.height < img_instance.width:
                target_width = int(lg / aspect_ratio)
                target_width_thumb = int(sm / aspect_ratio)
                img = img_instance.resize((target_width, lg), Image.Resampling.LANCZOS)
                thmb = img_instance.resize((target_width_thumb, sm), Image.Resampling.LANCZOS)
            else:
                img = img_instance.resize((lg, lg), Image.Resampling.LANCZOS)
                thmb = img_instance.resize((sm, sm), Image.Resampling.LANCZOS)
            
            original_filename = os.path.splitext(os.path.basename(self.original_image.path))[0]
            image_name = f"{images}{original_filename}.webp"
            thumb_name = f"{thumbnails}{original_filename}.webp"
            img_io = BytesIO()
            img.save(img_io, format='WEBP', quality=85)
            self.image.save(image_name, ContentFile(img_io.getvalue()), save=False)
            thumb_io = BytesIO()
            thmb.save(thumb_io, format='WEBP', quality=85)
            self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)
            os.remove(self.original_image.path)
            self.original_image = None

        super().save(*args, **kwargs)
