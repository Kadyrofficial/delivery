from rest_framework import serializers
from .models import Product
from catalogues.serializers import CatalogueForProductSerializer
from restaurants.serializers import RestaurantForProductSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'image', 'initial_price', 'discount', 'price', 'slug']

    def get_title(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"title_{lang}")

    def get_description(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"description_{lang}")

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)


class ProductRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    catalogue = CatalogueForProductSerializer()
    restaurant = RestaurantForProductSerializer()

    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'initial_price', 'discount', 'price', 'catalogue', "restaurant", 'slug']

    def get_title(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"title_{lang}")

    def get_description(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"description_{lang}")

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)
