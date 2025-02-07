from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from locations.models import CityProvince, EtrapCity, AddressLine
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('The Email or Phone number must be set')

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, password=password, **extra_fields)

class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)

class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_customer=True)

class DeliveryManManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delivery_man=True)

class RestaurantCustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_restaurant_customer=True)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_delivery_man = models.BooleanField(default=False)
    is_restaurant_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    city_province = models.ForeignKey(CityProvince, verbose_name="CityProvince", on_delete=models.CASCADE, related_name="user_city_province", blank=True, null=True)
    etrap_city = models.ForeignKey(EtrapCity, verbose_name="EtrapCity", on_delete=models.CASCADE, related_name="user_etrap_city", blank=True, null=True)
    address_line = models.ForeignKey(AddressLine, verbose_name="AddressLine", on_delete=models.CASCADE, related_name="user_address_line", blank=True, null=True)
    
    objects = UserManager()
    admins = AdminManager()
    customers = CustomerManager()
    delivery_men = DeliveryManManager()
    restaurant_customers = RestaurantCustomerManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def save(self, *args, **kwargs):
        if not self.email and not self.phone_number:
            raise ValueError('The Email or Phone number must be set')
        super().save(*args, **kwargs)
        
    def clean(self):
        if self.etrap_city and self.etrap_city.city_province != self.city_province:
            raise ValidationError("Selected Etrap City does not belong to the selected City Province.")

        if self.address_line and self.address_line.etrap_city != self.etrap_city:
            raise ValidationError("Selected Address Line does not belong to the selected Etrap City.")
    
    def __str__(self):
        return self.email if self.email else self.phone_number
