from rest_framework import serializers
from .models import Banner
from restaurants.serializers import RestaurantForBannerSerializer

class AppBannerSerializer(serializers.ModelSerializer):
    restaurant = RestaurantForBannerSerializer()
    
    class Meta:
        model = Banner
        fields = ['id', 'image', 'restaurant']


class WebBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image']
