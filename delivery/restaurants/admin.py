from django.contrib import admin
from .models import Restaurant
from products.models import Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", "description_tm", "description_ru", "image", "location", "address", "active_status", 'user']
    list_editable = ["title_tm", "title_ru", "description_tm", "description_ru", "image", "location", "address", "active_status", 'user']
    inlines = [ProductInline]

admin.site.register(Restaurant, RestaurantAdmin)
