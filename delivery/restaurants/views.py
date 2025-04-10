from rest_framework import viewsets
from .serializers import RestaurantSerializer, RestaurantListSerializer
from .models import Restaurant
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'

class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title_tm', 'title_ru']
    filterset_fields = ['is_top', 'is_delivery_free', 'is_new']
    pagination_class = Pagination
    
    def get_queryset(self):
        request = self.request
        location = request.headers.get('Location', 1) if request else 1
        return Restaurant.objects.filter(is_active=True, location=location)

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        return super().get_serializer_class()
