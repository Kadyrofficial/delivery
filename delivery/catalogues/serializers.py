from rest_framework import serializers
from .models import Catalogue


class CatalogueListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = Catalogue
        fields = ['id', 'title']
        
    def get_title(self, obj):
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', 'tm') if request else 'tm'
        return getattr(obj, f'title_{lang}', obj.title_tm)
