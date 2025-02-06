from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", "description_tm", "description_ru", "image", "catalogue", 'initial_price', "discount", "price", "restaurant", "active_status"]
    list_editable = ["title_tm", "title_ru", "description_tm", "description_ru", "image", "catalogue", 'initial_price', "discount", "restaurant", "active_status"]

admin.site.register(Product, ProductAdmin)
