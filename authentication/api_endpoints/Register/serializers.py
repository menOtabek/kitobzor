from rest_framework import serializers
from authentication.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('telegram_id',)
