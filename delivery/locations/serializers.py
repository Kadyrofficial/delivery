from rest_framework import serializers
from .models import Location, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AddressListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class AddressRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = Address
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class LocationListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class LocationRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    location = AddressListSerializer(many=True)
    
    class Meta:
        model = Location
        fields = ['id', 'title', 'location', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")
