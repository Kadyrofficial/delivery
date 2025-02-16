from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", "description_tm", "description_ru", "original_image", "initial_price", "discount", "restaurant", "catalogue", 'is_popular', 'is_special', "price"]
    list_editable = ["title_tm", "title_ru", "description_tm", "description_ru", "original_image", "initial_price", "restaurant", "catalogue", 'is_popular', 'is_special', "discount"]
    fieldsets = (
        ("Title", {"fields": ("title_tm", "title_ru")}),
        ("Description", {"fields": ("description_tm", "description_ru")}),
        ("Details", {"fields": ("original_image", 'image', 'thumbnail', "restaurant", "catalogue", "initial_price", "discount", 'price')}),
    )
    list_filter = ("restaurant", "catalogue")
    search_fields = ["title_tm", "title_ru", "description_tm", "description_ru"]
    readonly_fields = ('price', 'thumbnail', 'image')
admin.site.register(Product, ProductAdmin)
