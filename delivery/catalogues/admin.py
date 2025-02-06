from django.contrib import admin
from .models import Catalogue


class CatalogueAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru"]
    list_editable = ["title_tm", "title_ru"]

admin.site.register(Catalogue, CatalogueAdmin)
