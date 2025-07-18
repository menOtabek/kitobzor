from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    otp_code = serializers.RegexField(regex=r'^\d{6}$', error_messages={
        "invalid": "OTP code must be 6 digits"
    })
    phone_number = serializers.CharField(max_length=15)


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
