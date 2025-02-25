import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Catalogue


@receiver(post_delete, sender=Catalogue)
def delete_images_on_delete(sender, instance, **kwargs):
    try:
        os.remove(instance.original_image.path)
        os.remove(instance.image.path)
        os.remove(instance.thumbnail.path)
    except:
        pass
