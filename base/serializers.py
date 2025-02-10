from rest_framework import serializers
from .models import DefaultBookOffer

class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    region = serializers.PrimaryKeyRelatedField()
    name = serializers.CharField()


class DefaultBookOfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultBookOffer
        fields = ('user', 'book_name', 'book_author')

class DefaultBookOfferSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField()
    book_name = serializers.CharField()
    book_author = serializers.CharField()
