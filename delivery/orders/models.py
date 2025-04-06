from django.db import models
from accounts.models import User
from products.models import Product
from decimal import Decimal
from locations.models import Location, Address
from django.core.exceptions import ValidationError


class Order(models.Model):
    class Status(models.TextChoices):
        INACTIVE = 'inactive', 'Inactive'
        ACTIVE = 'active', 'Active'
        DECLINED = 'declined', 'Declined'
        SUCCESS = 'success', 'Success'

    user = models.ForeignKey(User, verbose_name="User of the order", on_delete=models.CASCADE, related_name='order')
    status = models.CharField(choices=Status, max_length=100, default=Status.INACTIVE)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False, blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name="Location", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Address", on_delete=models.CASCADE)
    delivery = models.ForeignKey(User, verbose_name="Delivery men", on_delete=models.CASCADE, blank=True, null=True, related_name='delivery_orders')
    
    def clean(self):
        if self.delivery and self.delivery.type != User.UserType.DELIVERY:
            raise ValidationError("The selected user is not a delivery person.")
        super().clean()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_price()

    def update_price(self, *args, **kwargs):
        self.total_price = self.order_item.aggregate(total=models.Sum('total_price'))['total'] or Decimal('0.00')
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(User, verbose_name="Ordered user", on_delete=models.CASCADE, related_name='order_item', editable=False, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name="Ordered product", on_delete=models.CASCADE, related_name='order_item')
    order = models.ForeignKey(Order, verbose_name="Order of the order item", on_delete=models.CASCADE, related_name='order_item')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False, blank=True, null=True)
     
    def save(self, *args, **kwargs):
        self.user = self.order.user
        self.total_price = Decimal(self.product.price) * Decimal(self.quantity)
        super().save(*args, **kwargs)
        self.order.update_price()
        

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_price()

    def __str__(self):
        return self.user.email
