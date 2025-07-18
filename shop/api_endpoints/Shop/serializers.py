from rest_framework import serializers

from shop.models import Shop
from utils.short_serializers import PointField


class ShopBaseSerializer(serializers.ModelSerializer):
    point = PointField()
    telegram_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'bio', 'picture', 'owner', 'star', 'district', 'telegram_url',
            'region', 'point', 'location_text', 'phone_number', 'telegram', 'is_active'
        )

    def get_telegram_url(self, obj):
        return obj.telegram_url


class ShopUpdateSerializer(ShopBaseSerializer):
    class Meta(ShopBaseSerializer.Meta):
        read_only_fields = ('id', 'owner', 'star')


class ShopDetailSerializer(ShopBaseSerializer):
    is_owner = serializers.BooleanField(read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    book_count = serializers.SerializerMethodField(read_only=True)

    class Meta(ShopBaseSerializer.Meta):
        fields = ShopBaseSerializer.Meta.fields + ('region_name', 'district_name', 'book_count', 'is_owner')

    def get_book_count(self, obj):
        return obj.book_count

    def get_is_owner(self, obj):
        user = self.context['request'].user
        return obj.owner == user


class ShopListSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Shop
        fields = ('id', 'name', 'picture', 'star', 'book_count')

    def get_book_count(self, obj):
        return obj.book_count
