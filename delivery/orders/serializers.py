from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product
from locations.models import Address, Location


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'order_item']

class OrderItemInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

class AddOrderSerializer(serializers.Serializer):
    order_item = serializers.ListField(child=OrderItemInputSerializer())

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        location_id = request.headers.get('Location')
        items_data = validated_data.pop('order_item')
        address_data = request.data.get('address')
        location = Location.objects.get(id=location_id)
        address = Address.objects.create(title=address_data, location=location)
        order = Order.objects.create(user=user, location=location, address=address)

        for item in items_data:
            product = item['product']
            quantity = item['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        return order