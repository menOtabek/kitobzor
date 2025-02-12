from rest_framework import serializers
from .models import User
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('telegram_id',)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp_code = serializers.IntegerField(required=True)

    def validate(self, data):
        if data.get('otp_code') and data.get('otp_code') < 100000 or data.get('otp_code') > 999999:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, 'Code is invalid')
