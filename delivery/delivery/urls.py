from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import CustomTokenView

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

    path('api/<str:lang>/products/', include('products.urls')),
    path('api/<str:lang>/catalogues/', include('catalogues.urls')),
    path('api/<str:lang>/restaurants/', include('restaurants.urls')),
    path('api/<str:lang>/locations/', include('locations.urls')),
    path('api/<str:lang>/accounts/', include('accounts.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    path('api/token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
