from django.contrib import admin
from .models import CityProvince, EtrapCity, AddressLine


# class CityProvinceInline(admin.TabularInline):
#     model = CityProvince
#     extra = 1



class EtrapCityInline(admin.TabularInline):
    model = EtrapCity
    extra = 1

class CityProvinceAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru"]
    list_editable = ["title_tm", "title_ru"]
    inlines = [EtrapCityInline]

admin.site.register(CityProvince, CityProvinceAdmin)


class AddressLineInline(admin.TabularInline):
    model = AddressLine
    extra = 1

class EtrapCityAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", "city_province"]
    list_editable = ["title_tm", "title_ru", "city_province"]
    inlines = [AddressLineInline]

admin.site.register(EtrapCity, EtrapCityAdmin)


class AddressLineAdmin(admin.ModelAdmin):
    list_display = ["id", "title_tm", "title_ru", "etrap_city"]
    list_editable = ["title_tm", "title_ru", "etrap_city"]

admin.site.register(AddressLine, AddressLineAdmin)
