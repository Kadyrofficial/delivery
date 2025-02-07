from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('phone_number')
        password = attrs.get('password')

        # First, try to authenticate using the default method (email or username)
        user = authenticate(username=username, password=password)

        if not user:
            # Check by phone number if not authenticated via email
            users = User.objects.filter(phone_number=username)
            if users.exists():
                if users.count() > 1:
                    raise serializers.ValidationError('Multiple users found with this phone number.')

                user = users.first()
                if not user.check_password(password):
                    raise serializers.ValidationError('Invalid credentials.')
            else:
                raise serializers.ValidationError('Invalid credentials.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        data = super().validate(attrs)
        data['user_id'] = user.id
        data['email'] = user.email
        data['phone_number'] = user.phone_number
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'is_active', 'city_province', 'etrap_city', 'address_line']
