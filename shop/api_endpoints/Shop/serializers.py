from rest_framework import serializers
from shop.models import Shop


class ShopBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'bio', 'picture', 'owner', 'star', 'district',
            'region', 'point', 'location_text', 'phone_number', 'telegram', 'is_active'
        )

class ShopUpdateSerializer(ShopBaseSerializer):
    class Meta(ShopBaseSerializer.Meta):
        read_only_fields = ('owner', 'star')


class ShopDetailSerializer(ShopBaseSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta(ShopBaseSerializer.Meta):
        fields = ShopBaseSerializer.Meta.fields + ('region_name', 'district_name')


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'picture', 'star')
