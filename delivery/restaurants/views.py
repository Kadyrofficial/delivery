from rest_framework import viewsets
from .serializers import RestaurantSerializer, RestaurantListSerializer
from .models import Restaurant
from rest_framework import filters


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title_tm', 'title_ru']

    def get_queryset(self):
        request = self.request
        location = request.headers.get('Location', 1) if request else 1
        return Restaurant.objects.filter(is_active=True, location=location)

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        return super().get_serializer_class()