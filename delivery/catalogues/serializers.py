from rest_framework import serializers
from .models import Catalogue


class CatalogueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Catalogue
        fields = '__all__'


class CatalogueListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Catalogue
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"title_{lang}")


class CatalogueRetrieveSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subcatalogues = CatalogueListSerializer(many=True)

    class Meta:
        model = Catalogue
        fields = ['id', 'title', 'subcatalogues', 'slug']

    def get_title(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"title_{lang}")


class CatalogueForProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Catalogue
        fields = ['title', 'slug']

    def get_title(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"title_{lang}")
