from rest_framework import serializers
from .models import Catalogue

class CatalogueSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Catalogue
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"title_{lang}")
