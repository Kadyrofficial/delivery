from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'image', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)


class RestaurantRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'description', 'image', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")

    def get_description(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"description_{lang}")

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)
    

class RestaurantForProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['title', 'slug']

    def get_title(self, obj):
        lang = self.context.get("lang")
        return getattr(obj, f"title_{lang}")
