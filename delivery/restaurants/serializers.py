from rest_framework import serializers
from .models import Restaurant
from products.serializers import ProductSerializer


class RestaurantListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'image', 'is_top', 'is_delivery_free', 'is_online', 'slug']
        
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumbnail.url)


class RestaurantSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    most_popular = serializers.SerializerMethodField()
    special_offers = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'image', 'slug', 'is_online', 'most_popular', 'special_offers']
        
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumbnail.url)
        
    def get_most_popular(self, obj):
        queryset = obj.products.filter(is_active=True, is_popular=True)
        return ProductSerializer(queryset, many=True, context=self.context).data
    
    def get_special_offers(self, obj):
        queryset = obj.products.filter(is_active=True, is_special=True)
        return ProductSerializer(queryset, many=True, context=self.context).data


class RestaurantForBannerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'slug']
        
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)
