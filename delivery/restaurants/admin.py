from django.contrib import admin
from .models import Restaurant
from products.models import Product


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_tm', 'title_ru', 'phone_number', 'original_image', 'location', 'address', 'is_active', 'is_online', 'is_top', 'is_delivery_free', 'is_new', 'user']
    list_editable = ['title_tm', 'title_ru', 'phone_number', 'original_image', 'location', 'address', 'is_active', 'is_online', 'is_top', 'is_delivery_free', 'is_new', 'user']
    fieldsets = (
        ('Title', {'fields': ('title_tm', 'title_ru')}),
        ('Details', {'fields': ('phone_number', 'original_image', 'image', 'thumbnail', 'location', 'address', 'user', 'is_active', 'is_online', 'is_top', 'is_delivery_free', 'is_new')}),
    )
    readonly_fields = ('image', 'thumbnail')
    list_filter = ['location', 'is_active', 'is_online', 'is_top', 'is_delivery_free', 'is_new']
    inlines = [ProductInline]
admin.site.register(Restaurant, RestaurantAdmin)
