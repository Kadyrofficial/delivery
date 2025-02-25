from rest_framework import serializers
from .models import Restaurant
from products.serializers import ProductLessDetailSerializer
from catalogues.serializers import CatalogueListSerializer, CatalogueSerializer
# APP

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
        view = self.context.get('view')
        
        if getattr(view, 'action', '') == 'list':
            return request.build_absolute_uri(obj.thumbnail.url)
        elif getattr(view, 'action', '') == 'retrieve':
            return request.build_absolute_uri(obj.image.url)
    

class RestaurantListStaticSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'title_tm', 'title_ru', 'image', 'is_top', 'is_delivery_free', 'is_online', 'slug']


    def get_image(self, obj):
        request = self.context.get('request')
        view = self.context.get('view')
        
        if getattr(view, 'action', '') == 'list':
            return request.build_absolute_uri(obj.thumbnail.url)
        elif getattr(view, 'action', '') == 'retrieve':
            return request.build_absolute_uri(obj.image.url)


class RestaurantSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    most_popular = serializers.SerializerMethodField()
    special_offers = serializers.SerializerMethodField()
    catalogues_list = serializers.SerializerMethodField()
    catalogues = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'image', 'is_online', 'catalogues_list', 'most_popular', 'special_offers', 'catalogues']
        
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)

    def get_image(self, obj):
        request = self.context.get('request')
        view = self.context.get('view')
        
        if getattr(view, 'action', '') == 'list':
            return request.build_absolute_uri(obj.thumbnail.url)
        elif getattr(view, 'action', '') == 'retrieve':
            return request.build_absolute_uri(obj.image.url)
        
    def get_most_popular(self, obj):
        queryset = obj.products.filter(is_active=True, is_popular=True)
        return ProductLessDetailSerializer(queryset, many=True, context=self.context).data
    
    def get_special_offers(self, obj):
        queryset = obj.products.filter(is_active=True, is_special=True)
        return ProductLessDetailSerializer(queryset, many=True, context=self.context).data
    
    def get_catalogues_list(self, obj):
        queryset = obj.catalogues.all()
        return CatalogueListSerializer(queryset, many=True, context=self.context).data
    
    def get_catalogues(self, obj):
        queryset = obj.catalogues.all()
        return CatalogueSerializer(queryset, many=True, context=self.context).data

# WEB

class WebRestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'title_tm', 'title_ru', 'image', 'slug']
