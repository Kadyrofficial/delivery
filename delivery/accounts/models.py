from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from locations.models import Location, Address
from django.core.exceptions import ValidationError
import uuid


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
    
def account_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"accounts/{uuid.uuid4().hex[:12]}.{ext}"

def account_car_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"cars/{uuid.uuid4().hex[:12]}.{ext}"

class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        STAFF = 'staff', "Staff"
        Admin = 'admin', "Admin"
        CUSTOMER = 'customer', "Customer"
        DELIVERY = 'delivery', "Delivery"
        CLIENT = 'client', "Client"
        
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    type = models.CharField(max_length=100, choices=UserType.choices, default=UserType.CUSTOMER)
    date_joined = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(Location, verbose_name="Location", on_delete=models.CASCADE, related_name="user_location", blank=True, null=True)
    address = models.ForeignKey(Address, verbose_name="Address", on_delete=models.CASCADE, related_name="user_address", blank=True, null=True)
    image = models.ImageField(upload_to=account_image_upload_path, blank=True, null=True)
    car_number = models.CharField(max_length=100, blank=True, null=True)
    car_image = models.ImageField(upload_to=account_car_image_upload_path, blank=True, null=True)
    car_color = models.CharField(max_length=100, blank=True, null=True)
    car_name = models.CharField(max_length=100, blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def save(self, *args, **kwargs):
        if not self.email and not self.phone_number:
            raise ValueError('The Email or Phone number must be set')
        super().save(*args, **kwargs)
        
    def clean(self):
        if self.is_staff == True and self.type != self.UserType.STAFF:
            raise ValidationError("Staff must be is_staff True")
        if self.type == self.UserType.STAFF and self.is_staff != True:
            raise ValidationError("Staff must be is_staff True")
        if self.address and self.address.location != self.address:
            raise ValidationError("Selected Address Line does not belong to the selected Etrap City.")
    
    def __str__(self):
        return self.email if self.email else self.phone_number


class Code(models.Model):
    user = models.ForeignKey(User, verbose_name="User of the Verification Code", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        return timezone.now() - self.created_at < timezone.timedelta(minutes=1)
