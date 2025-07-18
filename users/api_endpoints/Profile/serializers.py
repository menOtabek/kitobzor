from rest_framework import serializers

from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'bio', 'app_phone_number', 'role', 'first_name', 'last_name',
                  'picture', 'region', 'district', 'point', 'location_text', 'user_type')

    def get_user_type(self, obj):
        return obj.user_type
