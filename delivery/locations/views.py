from rest_framework import viewsets
from .models import CityProvince, EtrapCity, AddressLine
from .serializers import CityProvinceSerializer, CityProvinceListSerializer, CityProvinceRetrieveSerializer, EtrapCitySerializer, EtrapCityListSerializer, EtrapCityRetrieveSerializer, AddressLineSerializer, AddressLineListSerializer, AddressLineRetrieveSerializer
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUserOrReadOnly


class CityProvincePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class CityProvinceViewSet(viewsets.ModelViewSet):
    queryset = CityProvince.objects.all()
    lookup_field = "slug"
    pagination_class = CityProvincePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title_tm', 'title_ru']
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = CityProvinceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return CityProvinceListSerializer
        if self.action == "retrieve":
            return CityProvinceRetrieveSerializer
        return super().get_serializer_class()


class EtrapCityPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class EtrapCityViewSet(viewsets.ModelViewSet):
    queryset = EtrapCity.objects.all()
    lookup_field = "slug"
    pagination_class = EtrapCityPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title_tm', 'title_ru']
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = EtrapCitySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return EtrapCityListSerializer
        if self.action == "retrieve":
            return EtrapCityRetrieveSerializer
        return super().get_serializer_class()


class AddressLinePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class AddressLineViewSet(viewsets.ModelViewSet):
    queryset = AddressLine.objects.all()
    lookup_field = "slug"
    pagination_class = AddressLinePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title_tm', 'title_ru']
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = AddressLineSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AddressLineListSerializer
        if self.action == "retrieve":
            return AddressLineRetrieveSerializer
        return super().get_serializer_class()
