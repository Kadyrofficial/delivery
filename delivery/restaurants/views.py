from rest_framework import viewsets, filters
from .models import Restaurant
from .serializers import RestaurantSerializer, RestaurantListSerializer, RestaurantRetrieveSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUserOrReadOnly


class RestaurantPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    lookup_field = "slug"
    pagination_class = RestaurantPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city_province', 'etrap_city', 'active_status', ]
    search_fields = ['title_tm', 'title_ru']
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = RestaurantSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RestaurantListSerializer
        if self.action == "retrieve":
            return RestaurantRetrieveSerializer
        return super().get_serializer_class()
