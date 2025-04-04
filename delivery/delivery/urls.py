from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from accounts.views import UserViewSet
from restaurants.views import RestaurantViewSet
from products.views import ProductViewSet
from banners.views import AppBannerViewSet
from locations.views import LocationViewSet
from orders.views import OrderViewSet


router = routers.DefaultRouter()
router.register(r'accounts', UserViewSet, basename='accounts')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'banners', AppBannerViewSet, basename='banners')
router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'locations', LocationViewSet, basename='locations')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
