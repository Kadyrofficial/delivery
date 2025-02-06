from django.contrib import admin
from .models import Restaurant
from products.models import Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", "description_tm", "description_ru", "image", "city_province", "etrap_city", "address_line", "active_status"]
    list_editable = ["title_tm", "title_ru", "description_tm", "description_ru", "image", "city_province", "etrap_city", "address_line", "active_status"]
    inlines = [ProductInline]

admin.site.register(Restaurant, RestaurantAdmin)
