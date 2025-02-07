from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer, ProductRetrieveSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUserOrReadOnly


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.active_products.all()
    lookup_field = "slug"
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['catalogue', 'restaurant']
    search_fields = ['title_tm', 'title_ru']
    ordering_fields = ['price', 'discount']
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductRetrieveSerializer
        return super().get_serializer_class()
