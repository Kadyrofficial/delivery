from rest_framework import viewsets
from .models import Location, Address
from .serializers import LocationSerializer, LocationListSerializer, LocationRetrieveSerializer, AddressSerializer, AddressListSerializer, AddressRetrieveSerializer
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUserOrReadOnly


class LocationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    lookup_field = "slug"
    pagination_class = LocationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title_tm', 'title_ru']
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = LocationSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return LocationListSerializer
        if self.action == "retrieve":
            return LocationRetrieveSerializer
        return super().get_serializer_class()


class AddressPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    lookup_field = "slug"
    pagination_class = AddressPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title_tm', 'title_ru']
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = AddressSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AddressListSerializer
        if self.action == "retrieve":
            return AddressRetrieveSerializer
        return super().get_serializer_class()
