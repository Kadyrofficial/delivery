from django.contrib import admin
from .models import Catalogue
from products.models import Product


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

class CatalogueAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", 'original_image']
    list_editable = ["title_tm", "title_ru", 'original_image']
    fieldsets = (
        ("Title", {"fields": ("title_tm", "title_ru")}),
        ("Details", {"fields": ("original_image", "restaurant")}),
    )
    readonly_fields = ("restaurant", )
    inlines = [ProductInline]
admin.site.register(Catalogue, CatalogueAdmin)
