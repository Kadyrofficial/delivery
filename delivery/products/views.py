from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from catalogues.models import Catalogue


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.active_products.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['catalogue', 'restaurant']
    search_fields = ['title_tm', 'title_ru']
    ordering_fields = ['price', 'discount']

    # def get_filtered_queryset(self, request):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     catalogue_id = request.query_params.get('catalogue')

    #     if catalogue_id:
    #         catalogue = get_object_or_404(Catalogue, id=catalogue_id)

    #         # Get all subcategories recursively
    #         def get_subcatalogues(cat):
    #             subcatalogues = list(cat.subcatalogues.all())
    #             for sub in subcatalogues:
    #                 subcatalogues.extend(get_subcatalogues(sub))
    #             return subcatalogues
            
    #         all_catalogues = get_subcatalogues(catalogue) + [catalogue]
    #         queryset = queryset.filter(catalogue__in=all_catalogues)

    #         if not queryset.exists():
    #             all_subcatalogues = get_subcatalogues(catalogue)
    #             queryset = Product.active_products.filter(catalogue__in=all_subcategories)
            
    #         return queryset
        
    @swagger_auto_schema(
        operation_description="List of all Products",
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, lang):
        queryset = self.filter_queryset(self.get_queryset())
    
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'lang': lang, "request": request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'lang': lang, "request": request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Details of Selected Product",
        responses={200: ProductSerializer()}
    )
    def retrieve(self, request, lang, slug):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'lang': lang, "request": request})
        return Response(serializer.data)
