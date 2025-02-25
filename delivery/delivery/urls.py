from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from accounts.views import UserViewSet
from restaurants.views import RestaurantViewSet, WebRestaurantViewSet
from products.views import ProductViewSet
from banners.views import AppBannerViewSet, WebBannerViewSet
from locations.views import LocationViewSet


router = routers.DefaultRouter()
router.register(r'accounts', UserViewSet, basename='accounts')
router.register(r'banners', AppBannerViewSet, basename='banners')
router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'locations', LocationViewSet, basename='locations')

# web_api = routers.DefaultRouter()
# web_api.register(r'banners', WebBannerViewSet, basename='banners')
# web_api.register(r'restaurants', WebRestaurantViewSet, basename='restaurants')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('web_api/', include(web_api.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
