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


app_router = routers.DefaultRouter()
app_router.register(r'accounts', UserViewSet, basename='accounts')
app_router.register(r'banners', AppBannerViewSet, basename='banners')
app_router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
app_router.register(r'products', ProductViewSet, basename='products')
app_router.register(r'locations', LocationViewSet, basename='locations')

# web_api = routers.DefaultRouter()
# web_api.register(r'banners', WebBannerViewSet, basename='banners')
# web_api.register(r'restaurants', WebRestaurantViewSet, basename='restaurants')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_api/', include(app_router.urls)),
    # path('web_api/', include(web_api.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
