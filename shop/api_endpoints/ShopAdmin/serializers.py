from rest_framework import serializers
from shop.models import ShopStuff


class ShopStuffSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = ShopStuff
        fields = ('id', 'shop', 'shop_name', 'user', 'user_name', 'is_active')
