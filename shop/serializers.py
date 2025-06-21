from rest_framework import serializers
from .models import Shop


class ShopShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'picture')
