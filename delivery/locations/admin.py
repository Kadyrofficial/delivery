from django.contrib import admin
from .models import Location, Address


class AddressLineInline(admin.TabularInline):
    model = Address
    extra = 1

class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru"]
    list_editable = ["title_tm", "title_ru"]
    inlines = [AddressLineInline]

admin.site.register(Location, LocationAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", "location"]
    list_editable = ["title_tm", "title_ru", "location"]

admin.site.register(Address, AddressAdmin)
