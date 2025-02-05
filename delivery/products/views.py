from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    @swagger_auto_schema(
        operation_description="List of all Products",
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, lang):
        queryset = self.filter_queryset(self.get_queryset())
    
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

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
