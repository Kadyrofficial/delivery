from django.contrib import admin
from .models import User, Code


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "location", "address", 'type']
    list_editable = ["email", "phone_number", "first_name", "last_name", "is_active", "is_staff", "date_joined", "location", "address", 'type']
    list_filter = ['type']
    
admin.site.register(User, UserAdmin)


class CodeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "code"]
    
admin.site.register(Code, CodeAdmin)
