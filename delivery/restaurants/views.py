from rest_framework import viewsets
from .serializers import RestaurantSerializer, RestaurantListSerializer, RestaurantListStaticSerializer, WebRestaurantListSerializer
from .models import Restaurant
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title_tm', 'title_ru']
    filterset_fields = ['is_top', 'is_delivery_free', 'is_new']
    
    def get_queryset(self):
        request = self.request
        location = request.headers.get('Location', 1) if request else 1
        return Restaurant.objects.filter(is_active=True, location=location)

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        return super().get_serializer_class()


class WebRestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = WebRestaurantListSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title_tm', 'title_ru']
    filterset_fields = ['is_top', 'is_delivery_free', 'is_new']
    
    def get_queryset(self):
        request = self.request
        location = request.headers.get('Location', 1) if request else 1
        return Restaurant.objects.filter(is_active=True, location=location)

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer if self.request.headers.get('Location') else RestaurantListStaticSerializer
        return super().get_serializer_class()