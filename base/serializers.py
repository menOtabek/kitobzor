from rest_framework import serializers
from .models import DefaultBookOffer, Region, District


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'region')

class DefaultBookOfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultBookOffer
        fields = ('user', 'book_name', 'book_author')


class DefaultBookOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultBookOffer
        fields = ('id', 'user', 'book_name', 'book_author')
