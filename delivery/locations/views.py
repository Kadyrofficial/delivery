from rest_framework import viewsets, mixins
from .serializers import LocationSerializer
from .models import Location


class LocationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
