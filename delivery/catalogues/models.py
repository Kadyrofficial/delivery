import os
from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.utils import timezone
from restaurants.models import Restaurant


class Catalogue(models.Model):
    title_tm = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    thumbnail = models.ImageField(null=True, blank=True, editable=False)
    image = models.ImageField(null=True, blank=True, editable=False)
    original_image = models.ImageField()
    date_added = models.DateTimeField(blank=True, null=True, editable=False)
    restaurant = models.ManyToManyField(Restaurant, verbose_name="Restaurants", related_name='catalogues', editable=False)
    is_popular = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title_tm

    def save(self, lg=1000, sm=400, originals='catalogues/originals/', images='catalogues/images/', thumbnails='catalogues/thumbnails/', *args, **kwargs):
        self.slug = unidecode(slugify(self.title_tm))
        if not self.pk:
            self.date_added = timezone.now()

        if not os.path.exists(self.original_image.path):
            try:
                old_instance = Catalogue.objects.get(pk=self.pk)
                os.remove(old_instance.original_image.path)
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
        super().save(*args, **kwargs)
