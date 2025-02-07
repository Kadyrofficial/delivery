from django.contrib import admin
from .models import User
from restaurants.models import Restaurant


admin.site.register(User)


class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
        
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    list_editable = ["email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    
    def get_queryset(self, request):
        return User.admins.all()

admin.site.register(AdminUser, AdminUserAdmin)


class CustomerUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    list_editable = ["email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    
    def get_queryset(self, request):
        return User.customers.all()

admin.site.register(CustomerUser, CustomerUserAdmin)


class DeliveryManUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Delivery Man'
        verbose_name_plural = 'Delivery Men'

class DeliveryManUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    list_editable = ["email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    
    def get_queryset(self, request):
        return User.delivery_men.all()

admin.site.register(DeliveryManUser, DeliveryManUserAdmin)


class RestaurantCustomerUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Restaurant Customer'
        verbose_name_plural = 'Restaurant Customers'

class RestaurantInline(admin.TabularInline):
    model = Restaurant
    extra = 1

class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    list_editable = ["email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "city_province", "etrap_city", "address_line"]
    inlines = [RestaurantInline]
    
    def get_queryset(self, request):
        return User.restaurant_customers.all()

admin.site.register(RestaurantCustomerUser, CustomerUserAdmin)
