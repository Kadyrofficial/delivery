from rest_framework import serializers
from .models import CityProvince, EtrapCity, AddressLine


class AddressLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressLine
        fields = '__all__'


class AddressLineListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = AddressLine
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class AddressLineRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = AddressLine
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class EtrapCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EtrapCity
        fields = '__all__'


class EtrapCityListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = EtrapCity
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class EtrapCityRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    address_line = AddressLineListSerializer(many=True)
    
    class Meta:
        model = EtrapCity
        fields = ['id', 'title', 'address_line', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class CityProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityProvince
        fields = '__all__'


class CityProvinceListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = CityProvince
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")


class CityProvinceRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    etrap_city = EtrapCityListSerializer(many=True)
    
    class Meta:
        model = CityProvince
        fields = ['id', 'title', 'etrap_city', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")
