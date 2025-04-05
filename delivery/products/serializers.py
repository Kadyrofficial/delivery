from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'initial_price', 'discount', 'discount_state', 'restaurant', 'price', 'slug']
    
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)

    def get_description(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'description_{lang}', obj.description_tm)
    
    def get_restaurant(self, obj):
        return obj.restaurant.slug
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request and obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None 
