from rest_framework import serializers
from authentication.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'bio', 'app_phone_number', 'first_name', 'last_name', 'username',
                  'picture', 'region', 'district', 'point', 'location_text')


__all__ = ['UserUpdateSerializer']
