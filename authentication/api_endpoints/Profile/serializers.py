from rest_framework import serializers
from authentication.models import User
from authentication.api_endpoints.OtherProfile.serializers import BookUserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'bio', 'app_phone_number', 'role', 'first_name', 'last_name',
                  'picture', 'region', 'district', 'point', 'location_text', 'books',)

    def get_books(self, obj):
        return BookUserSerializer(obj.book_user.filter(is_banned=False), many=True, context=self.context).data
