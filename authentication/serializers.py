from rest_framework import serializers
from .models import User
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('telegram_id',)


class BotUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'phone_number', 'first_name', 'last_name', 'telegram_language')

        extra_kwargs = {
            'id': {'read_only': True, 'required': True},
            'telegram_id': {'required': True, 'read_only': True},
            'telegram_language': {'required': False},
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GetLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'telegram_language', 'phone_number')

        extra_kwargs = {
            'telegram_id': {'required': True, 'read_only': True},
            'telegram_language': {'required': False},
            'phone_number': {'required': False},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'bio', 'phone_is_visible', 'first_name', 'last_name',
                  'picture', 'region', 'district', 'location', 'location_is_visible')
        extra_kwargs = {
            'id': {'read_only': True, 'required': True},
            'bio': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'picture': {'required': False},
            'region': {'required': False},
            'district': {'required': False},
            'location': {'required': False}
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6)

    def validate(self, data):
        if data.get('otp_code') and len(data.get('otp_code')) != 6:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, 'Code is invalid')
        return data


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        try:
            token = RefreshToken(data.get('refresh_token'))
        except Exception as e:
            raise serializers.ValidationError(str(e))
        if token.get('exp') < timezone.now().timestamp():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, 'Refresh token is expired')
        return data


class BookUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(required=False, read_only=True)
    picture = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(required=False, read_only=True)

    def get_picture(self, obj):
        request = self.context.get('request')
        if obj.picture:
            return request.build_absolute_uri(obj.picture.url) if request else obj.picture.url
        return None


class PostUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(required=False, read_only=True)
    book_name = serializers.CharField(required=False, read_only=True)
    book_author = serializers.CharField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)
    is_active = serializers.BooleanField(required=False, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'phone_is_visible', 'role', 'first_name', 'last_name',
                  'picture', 'region', 'district', 'location', 'location_is_visible', 'books', 'posts')

    def get_books(self, obj):
        return BookUserSerializer(obj.book_user.filter(is_banned=False), many=True, context=self.context).data

    def get_posts(self, obj):
        return PostUserSerializer(obj.post_user.filter(is_banned=False), many=True, context=self.context).data


class UserOtherPhoneLocationSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture',
                  'region', 'district', 'location', 'books', 'posts')

    def get_books(self, obj):
        return BookUserSerializer(obj.book_user.filter(is_banned=False), many=True, context=self.context).data

    def get_posts(self, obj):
        return PostUserSerializer(obj.post_user.filter(is_banned=False), many=True, context=self.context).data


class UserOtherPhoneSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture',
                  'region', 'district', 'location', 'books', 'posts')

    def get_location(self, obj):
        return

    def get_books(self, obj):
        return BookUserSerializer(obj.book_user.filter(is_banned=False), many=True, context=self.context).data

    def get_posts(self, obj):
        return PostUserSerializer(obj.post_user.filter(is_banned=False), many=True, context=self.context).data


class UserOtherLocationSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture',
                  'region', 'district', 'location', 'books', 'posts')

    def get_phone_number(self, obj):
        return

    def get_books(self, obj):
        return BookUserSerializer(obj.book_user.filter(is_banned=False), many=True, context=self.context).data

    def get_posts(self, obj):
        return PostUserSerializer(obj.post_user.filter(is_banned=False), many=True, context=self.context).data


class UserOtherSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture', 'region',
                  'district', 'location', 'books', 'posts')

    def get_phone_number(self, obj):
        return

    def get_location(self, obj):
        return

    def get_books(self, obj):
        return BookUserSerializer(obj.book_user.filter(is_banned=False), many=True, context=self.context).data

    def get_posts(self, obj):
        return PostUserSerializer(obj.post_user.filter(is_banned=False), many=True, context=self.context).data


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number')
