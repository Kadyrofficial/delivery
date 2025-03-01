from rest_framework import viewsets, mixins
from .serializers import AppBannerSerializer
from .models import Banner


class AppBannerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Banner.objects.all()
    serializer_class = AppBannerSerializer
