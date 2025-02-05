from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["title", 'slug']

    def get_title(self, obj):
        lang = self.context.get('lang')
        return getattr(obj, f"title_{lang}")
