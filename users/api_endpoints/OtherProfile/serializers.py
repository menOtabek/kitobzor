from rest_framework import serializers

from users.models import User


class UserOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'bio', 'app_phone_number', 'first_name', 'last_name', 'picture', 'region',
                  'district', 'point', 'location_text')
