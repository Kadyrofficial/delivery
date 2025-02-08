from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserLessDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'location', 'address', 'image', 'car_number', 'car_image', 'car_color', 'car_name']


class AuthSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    phone_number = serializers.CharField(max_length=15, required=False)
    code = serializers.CharField(max_length=6, required=False)
    password = serializers.CharField(required=False)
    forgot_password = serializers.BooleanField(required=False)
