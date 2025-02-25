from django.contrib import admin
from .models import Location, Address


class AddressLineInline(admin.TabularInline):
    model = Address
    extra = 1

class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", 'queue']
    list_editable = ["title_tm", "title_ru", 'queue']
    ordering = ['queue']
    inlines = [AddressLineInline]

admin.site.register(Location, LocationAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "location"]
    list_editable = ["title", "location"]
    list_filter = ('location',)
admin.site.register(Address, AddressAdmin)
