from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

    
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
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)


admin.site.unregister(Group)
