import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Product


@receiver(post_delete, sender=Product)
def delete_images_on_delete(sender, instance, **kwargs):
    try:
        os.remove(instance.original_image.path)
        os.remove(instance.image.path)
        os.remove(instance.thumbnail.path)
    except:
        pass
    old_catalogue = instance.catalogue
    old_restaurant = instance.restaurant
    if not Product.objects.filter(catalogue=old_catalogue, restaurant=old_restaurant).exists():
        old_catalogue.restaurant.remove(old_restaurant)
