from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "delivery", "total_price"]
    list_editable = ["status", "delivery"]
    fieldsets = (
        ("Details", {"fields": ("user", "total_price", "delivery", "location", "address")}),
    )
    list_filter = ("status", )
    search_fields = ["user"]
    readonly_fields = ('total_price', )
    inlines = [OrderItemInline]
admin.site.register(Order, OrderAdmin)
