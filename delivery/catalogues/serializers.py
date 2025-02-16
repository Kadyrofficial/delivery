from rest_framework import serializers
from .models import Catalogue
from products.serializers import ProductForCatalogueSerializer


class CatalogueListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = Catalogue
        fields = ['id', 'title']
        
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)


class CatalogueSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = Catalogue
        fields = ['id', 'title', 'products']
        
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)

    def get_products(self, obj):
        queryset = obj.product.all()
        return ProductForCatalogueSerializer(queryset, many=True, context=self.context).data
