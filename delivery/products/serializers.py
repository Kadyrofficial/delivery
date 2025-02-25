from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'initial_price', 'discount', 'price', 'slug']

    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)

    def get_description(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'description_{lang}', obj.description_tm)

    def get_image(self, obj):
        request = self.context.get('request')
        view = self.context.get('view')
        
        if getattr(view, 'action', '') == 'list':
            return request.build_absolute_uri(obj.thumbnail.url)
        elif getattr(view, 'action', '') == 'retrieve':
            return request.build_absolute_uri(obj.image.url)


class ProductLessDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'initial_price', 'discount', 'price', 'slug']
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_popular=True)
    
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)
    
    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumbnail.url)


class ProductForCatalogueSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'image', 'initial_price', 'discount', 'price', 'is_popular', 'slug']
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_popular=True)
    
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)
    
    def get_description(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'description_{lang}', obj.description_tm)
    
    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.thumbnail.url)