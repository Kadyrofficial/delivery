from django.contrib import admin
from .models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ["id", "original_image"]
    list_editable = ["original_image"]
    fieldsets = (
        ("Details", {"fields": ("original_image", 'image', 'thumbnail')}),
    )
    readonly_fields = ('thumbnail', 'image')
admin.site.register(Banner, BannerAdmin)
