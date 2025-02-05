from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response


class ProductViewSet(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def list(self, request, lang):
        queryset = self.filter_queryset(self.get_queryset())

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'lang': lang, "request": request})
        return Response(serializer.data)

    def retrieve(self, request, lang):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'lang': lang, "request": request})
        return Response(serializer.data)
