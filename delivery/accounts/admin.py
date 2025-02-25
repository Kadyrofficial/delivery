from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Order, OrderItem
from restaurants.models import Restaurant


class RestaurantInline(admin.TabularInline):
    model = Restaurant
    extra = 1
    
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone_number", "first_name", "last_name")
    list_editable = ("email", "phone_number", "first_name", "last_name")
    list_filter = ('type',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number')}),
        ('Info', {'fields': ('first_name', 'last_name')}),
        ('Address', {'fields': ('location', 'address')}),
        ('Details', {'fields': ('type', 'password', 'new_password', 'is_active', 'date_joined')}),
    )
    readonly_fields = ('date_joined', 'password')
    inlines = [RestaurantInline]
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "price", "date_added", 'status')
    list_editable = ('status', )
    list_filter = ('status',)
    # fieldsets = (
    #     (None, {'fields': ('email', 'phone_number')}),
    #     ('Info', {'fields': ('first_name', 'last_name')}),
    #     ('Details', {'fields': ('type', 'password', 'new_password', 'is_active', 'date_joined')}),
    # )
    readonly_fields = ("user", "price", 'date_added')
    inlines = [OrderItemsInline]
    # search_fields = ('email', 'phone_number', 'first_name', 'last_name')

admin.site.register(Order, OrderAdmin)


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "user", 'order', 'price')
    # list_filter = ('type',)
    fieldsets = (
        ('Info', {'fields': ('product', 'quantity')}),
        ('Details', {'fields': ('price', 'user', 'order',)}),
    )
    readonly_fields = ("order", 'price')

admin.site.register(OrderItem, OrderItemAdmin)


# admin.site.unregister(Group)