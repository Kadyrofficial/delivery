from django.urls import path, include
from rest_framework import routers
from .views import CityProvinceViewSet, EtrapCityViewSet, AddressLineViewSet


router = routers.DefaultRouter()
router.register(r'city_province', CityProvinceViewSet, basename="city-province")
router.register(r'etrap_city', EtrapCityViewSet, basename="city-etrap_city")
router.register(r'address_line', AddressLineViewSet, basename="city-address_line")

urlpatterns = [
    path('', include(router.urls)),
]
