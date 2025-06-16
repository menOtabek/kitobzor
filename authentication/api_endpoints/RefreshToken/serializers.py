from rest_framework import serializers
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        refresh_token = data.get('refresh_token')
        try:
            token = RefreshToken(refresh_token)
        except Exception as e:
            refresh_token.black_list()
            raise serializers.ValidationError(str(e))
        if token.get('exp') < timezone.now().timestamp():
            refresh_token.black_list()
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, 'Refresh token is expired')
        return data
