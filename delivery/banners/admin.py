from django.contrib import admin
from .models import Banner


# class BannerAdmin(admin.ModelAdmin):
#     list_display = ["id", "original_image", 'thumbnail', 'image', 'restaurant']
#     list_editable = ["original_image", 'restaurant']
#     fieldsets = (
#         ("Details", {"fields": ("original_image", 'image', 'thumbnail', 'restaurant')}),
#     )
#     readonly_fields = ('thumbnail', 'image')
# admin.site.register(Banner, BannerAdmin)
