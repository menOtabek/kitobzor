from rest_framework import serializers
from .models import User, Profile, Otp
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'bot_id')


class LoginSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        if data.get('otp_code') and len(data.get('otp_code')) != 6:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, 'Code is invalid')


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'first_name', 'last_name', 'picture', 'region', 'district', 'latitude', 'longitude')

        extra_kwargs = {
            'last_name': {'required': False},
            'picture': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False}
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture', 'region', 'district', 'latitude', 'longitude')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'picture': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
            'region': {'required': False},
            'district': {'required': False},
        }


class ProfileDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    picture = serializers.ImageField()
    region = serializers.PrimaryKeyRelatedField()
    district = serializers.PrimaryKeyRelatedField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
