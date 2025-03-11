from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title_tm', 'title_ru']
    filterset_fields = ['discount_state', 'restaurant']
    pagination_class = Pagination
    
    def get_queryset(self):
        request = self.request
        location = request.headers.get('Location', 1) if request else 1
        return Product.objects.filter(is_active=True, restaurant__location=location)

    def get_serializer_class(self):
        return ProductSerializer
    