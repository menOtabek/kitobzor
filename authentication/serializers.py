from rest_framework import serializers
from .models import User
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('telegram_id',)


class BotUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'phone_number', 'first_name', 'last_name')

        extra_kwargs = {
            'id': {'read_only': True, 'required': True},
            'telegram_id': {'required': True, 'read_only': True},
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'picture', 'region', 'district', 'latitude', 'longitude')
        extra_kwargs = {
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'picture': {'required': False},
            'region': {'required': False},
            'district': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
        }

        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp_code = serializers.IntegerField(required=True)

    def validate(self, data):
        if data.get('otp_code') and (data.get('otp_code') < 100000 or data.get('otp_code') > 999999):
            raise CustomApiException(ErrorCodes.INVALID_INPUT, 'Code is invalid')
        return data


class OtpGenerateSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    role = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        try:
            token = RefreshToken(data.get('refresh_token'))
        except Exception as e:
            raise serializers.ValidationError(str(e))
        if token.get('exp') < timezone.now().timestamp():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, 'Refresh token is expired')
        return data
