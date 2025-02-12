from rest_framework import serializers
from .models import User
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('telegram_id',)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'phone_number', 'first_name', 'last_name',
                  'login_time', 'region', 'district', 'otp_code', 'picture', 'latitude', 'longitude')

        extra_kwargs = {
            'telegram_id': {'required': True},
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'otp_code': {'required': False},
            'region': {'required': False},
            'district': {'required': False},
            'login_time': {'required': False},
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


class OtpGenerateSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
