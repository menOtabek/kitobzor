from rest_framework import serializers

from authentication.models import User


class GetLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'language', 'phone_number')

        extra_kwargs = {
            'telegram_id': {'required': True, 'read_only': True},
        }
