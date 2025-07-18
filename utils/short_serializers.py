from rest_framework import serializers
from django.contrib.gis.geos import Point

from base.models import Region, District
from users.models import User
from shop.models import Shop
from sharing.models import Book



class ShopShortSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()
    class Meta:
        model = Shop
        fields = ('id', 'name', 'picture', 'star', 'book_count', 'phone_number')

    def get_book_count(self, obj):
        return obj.book_count



class RegionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')



class DistrictShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name')


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'picture', 'app_phone_number')


class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'picture', 'price')


class PointField(serializers.Field):
    def to_internal_value(self, data):
        import json
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid JSON format.")

        if isinstance(data, dict):
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            if latitude is None or longitude is None:
                raise serializers.ValidationError("Both 'latitude' and 'longitude' are required.")
            return Point(longitude, latitude)
        raise serializers.ValidationError("Invalid input type. Expected a dictionary or Point.")

    def to_representation(self, value):
        if isinstance(value, Point):
            return {"latitude": value.y, "longitude": value.x}
        return None
