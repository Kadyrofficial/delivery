from rest_framework import viewsets
from .models import Catalogue
from .serializers import CatalogueSerializer, CatalogueListSerializer, CatalogueRetrieveSerializer
from rest_framework.permissions import IsAdminUserOrReadOnly


class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        if self.action == "list":
            return Catalogue.head_catalogues.all()
        return super().get_queryset()
    
    def get_serializer_class(self):
        if self.action == "list":
            return CatalogueListSerializer
        if self.action == "retrieve":
            return CatalogueRetrieveSerializer
        return super().get_serializer_class()
