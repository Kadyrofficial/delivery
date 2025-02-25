from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    def get_queryset(self):
        request = self.request
        location = request.headers.get('Location', 1) if request else 1
        return Product.objects.filter(is_active=True)

    def get_serializer_class(self):
        return ProductSerializer