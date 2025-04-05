from django.contrib import admin
from .models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", 'queue']
    list_editable = ["title_tm", "title_ru", 'queue']
    ordering = ['queue']

admin.site.register(Location, LocationAdmin)
