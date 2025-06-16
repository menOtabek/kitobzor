from rest_framework import serializers
from authentication.models import User


class BotUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'phone_number', 'first_name', 'last_name', 'language')
