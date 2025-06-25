from rest_framework import serializers

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class LoginSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True, max_length=6)
    phone_number = serializers.CharField(required=True, max_length=15)

    def validate(self, data):
        otp_code = data.get('otp_code')
        if otp_code and len(str(otp_code)) != 6:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, 'Code is invalid')
        return data


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
