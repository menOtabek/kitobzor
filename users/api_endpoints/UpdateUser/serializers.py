from rest_framework import serializers
from users.models import User
from utils.short_serializers import PointField


class UserUpdateSerializer(serializers.ModelSerializer):
    point = PointField()
    class Meta:
        model = User
        fields = (
            'id', 'bio', 'app_phone_number', 'first_name', 'last_name', 'username',
            'picture', 'region', 'district', 'point', 'location_text'
        )
        read_only_fields = ('id',)

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(id=user.id).filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value
