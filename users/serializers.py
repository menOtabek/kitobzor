from rest_framework import serializers
from users.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'picture', 'first_name', 'last_name')
