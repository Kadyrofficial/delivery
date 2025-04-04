from rest_framework import viewsets
from .serializers import OrderSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)