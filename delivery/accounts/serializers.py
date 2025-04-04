from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=[])
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'new_password', 'is_active', 'type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            
            if request.user.type == User.UserType.SUPERUSER:
                self.fields['type'].choices = User.UserType
            else:
                self.fields['type'].choices = [
                    (User.UserType.CLIENT),
                    (User.UserType.DELIVERY),
                    (User.UserType.CUSTOMER)
                ]
        if request and request.method == 'PUT':
            if request.user.type != User.UserType.SUPERUSER:
                self.fields.pop('type', None)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name']
        
class AuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    code = serializers.CharField(max_length=6, required=False)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    
class VerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField(max_length=6)