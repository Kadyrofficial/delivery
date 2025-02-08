from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from accounts.views import UserViewSet, AuthViewSet
from locations.views import LocationViewSet, AddressViewSet
from catalogues.views import CatalogueViewSet
from restaurants.views import RestaurantViewSet
from products.views import ProductViewSet


router = routers.DefaultRouter()

router.register(r'accounts/users', UserViewSet, basename="users")
router.register(r'accounts/auth', AuthViewSet, basename="auth")
router.register(r'locations/location', LocationViewSet, basename="location")
router.register(r'locations/address', AddressViewSet, basename="address")
router.register(r'catalogues', CatalogueViewSet, basename="catalogues")
router.register(r'restaurants', RestaurantViewSet, basename="restaurants")
router.register(r'products', ProductViewSet, basename="products")

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation of Delivery Platform",
        default_version='v1',
        description="For Front-End Developer Kerim Gullyyev",
        # terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="kadyr.gullyyew@gmail.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<str:lang>/', include(router.urls)),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
