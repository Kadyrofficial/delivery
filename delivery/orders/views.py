from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from .models import OrderItem
from .serializers import AddOrderSerializer, OrderItemSerializer
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    pagination_class = Pagination
    
    def get_queryset(self):
        return OrderItem.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    @action(methods=['post'], detail=False, url_path='add')
    @transaction.atomic
    def add(self, request):
        serializer = AddOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                user = request.user
                send_mail(
                    subject='New Order',
                    message=f'A new order is created by {user.email}',
                    from_email='kadyr.gullyyew@gmail.com',
                    recipient_list=['Gullyyevk@gmail.com'],
                    fail_silently=False,
                )
                order = serializer.save()
                return Response({
                    'message': 'Order created successfully.',
                    'order_id': order.id
                }, status=status.HTTP_201_CREATED)
            except:
                return Response({
                    'message': 'Order created successfully.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
