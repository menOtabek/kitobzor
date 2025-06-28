from rest_framework import serializers
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        raw_token = data.get('refresh_token')

        try:
            token = RefreshToken(raw_token)
        except TokenError as e:
            raise serializers.ValidationError({'refresh_token': 'Invalid token: ' + str(e)})


        if token.get('exp') < timezone.now().timestamp():
            try:
                token.blacklist()
            except Exception:
                pass
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, 'Refresh token is expired')

        try:
            token.blacklist()
        except Exception:
            pass

        return data
