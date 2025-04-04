from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']



class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'order_item']
