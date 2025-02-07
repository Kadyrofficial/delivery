from django.urls import path, include
from rest_framework import routers
from .views import RestaurantViewSet


router = routers.DefaultRouter()
router.register(r'', RestaurantViewSet, basename="restaurants")


urlpatterns = [
    path('', include(router.urls)),
]
