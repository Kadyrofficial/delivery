from rest_framework import routers
from django.urls import path, include
from .views import CatalogueViewSet


router = routers.DefaultRouter()
router.register(r'', CatalogueViewSet, basename="catalogues")

urlpatterns = [
    path("", include(router.urls))
]
