from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from products.models import Product
from django.core.validators import MinValueValidator
from locations.models import Location, Address
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        if email:
            email = self.normalize_email(email)
        extra_fields.setdefault('type', User.UserType.SUPERUSER)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save_super(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        SUPERUSER = 'superuser', 'Superuser'
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Client'
        DELIVERY = 'delivery', 'Delivery'
        CUSTOMER = 'customer', 'Customer'

    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField()
    type = models.CharField(max_length=50, choices=UserType, default=UserType.CUSTOMER)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    new_password = models.CharField(max_length=50, blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name="Location", on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, verbose_name="Address", on_delete=models.CASCADE, blank=True, null=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def clean(self):
        if not self.email and not self.phone_number:
            raise ValueError("The Email or Phone number must be set")

    def __str__(self):
        return self.email if self.email else self.phone_number
    
    def clean(self):
        if self.location and self.address and self.address.location != self.location:
            raise ValidationError("Selected Address Line does not belong to the selected Etrap City.")
        
    def save(self, *args, **kwargs):
        if self.type == self.UserType.SUPERUSER:
            self.is_superuser = True
            self.is_staff = True
        
        elif self.type == self.UserType.ADMIN:
            self.is_superuser = False
            self.is_staff = True
            super().save(*args, **kwargs)
            self.groups.set([1])
        else:
            self.is_superuser = False
            self.is_staff = False
        if self.new_password:
            self.set_password(self.new_password)
            self.new_password = None
        super().save(*args, **kwargs)

    def save_super(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Code(models.Model):
    user = models.ForeignKey(User, verbose_name="User", editable=False, on_delete=models.CASCADE)
    code = models.CharField(max_length=6 , editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def is_valid(self):
        return timezone.now() - self.date_created < timezone.timedelta(minutes=30)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ORDERED = 'active', 'Active'
        ACCEPTED = 'accepted', 'Accepted'
        DELIVERED = 'delivered', 'Delivered'
        REJECTED = 'rejected', 'Rejected'
        
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, editable=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.TextField(choices=OrderStatus, default=OrderStatus.PENDING)
    
    def save(self, *args, **kwargs):
        if self.status != self.OrderStatus.PENDING:
            if not (self.user.is_active and self.user.location and self.user.address and self.user.phone_number):
                raise ValueError("User must have location, address and phone_number")
        super().save(*args, **kwargs)
        self.update_price()
        
    def update_price(self, *args, **kwargs):
        self.price = sum(item.price for item in self.order_items.all())
        self.save(update_fields=['price'])

    def __str__(self):
        return f'Order of ({self.user.phone_number})'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE, related_name='order_items', editable=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=False)

    def __str__(self):
        return f'{self.user.phone_number} - {self.user.email}'

    def save(self, *args, **kwargs):
        if self.pk:
            order_item = OrderItem.objects.get(pk=self.pk)
            if order_item.order.status != Order.OrderStatus.PENDING:
                raise ValidationError('OrderItem cannot be modified, it is already ordered')
        self.price = self.product.price * self.quantity
        order, created = Order.objects.get_or_create(user=self.user, status=Order.OrderStatus.PENDING)
        self.order = order
        super().save(*args, **kwargs)
        if self.pk:
            self.order.update_price()

    def delete(self, *args, **kwargs):
        if not OrderItem.objects.filter(order=self.order).exists():
            self.order.delete()
        super().delete(*args, **kwargs)
