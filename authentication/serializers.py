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
        fields = ('id', 'telegram_id', 'phone_number', 'first_name', 'last_name')

        extra_kwargs = {
            'id': {'read_only': True, 'required': True},
            'telegram_id': {'required': True, 'read_only': True},
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_is_visible', 'first_name', 'last_name',
                  'picture', 'region', 'district', 'location', 'location_is_visible')
        extra_kwargs = {
            'id': {'read_only': True, 'required': True},
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
    otp_code = serializers.IntegerField(required=True)

    def validate(self, data):
        if data.get('otp_code') and (data.get('otp_code') < 100000 or data.get('otp_code') > 999999):
            raise CustomApiException(ErrorCodes.INVALID_INPUT, 'Code is invalid')
        return data


class OtpGenerateSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
    role = serializers.CharField()


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
    picture = serializers.CharField(required=False, read_only=True)


class PostUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    title = serializers.CharField(required=False, read_only=True)
    book_name = serializers.CharField(required=False, read_only=True)
    book_author = serializers.CharField(required=False, read_only=True)
    created_at = serializers.DateTimeField(required=False, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    posts = PostUserSerializer(many=True, required=False, source='post_user', read_only=True)
    books = BookUserSerializer(many=True, required=False, source='book_user', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'phone_is_visible', 'role', 'first_name', 'last_name',
                  'picture', 'region', 'district', 'location', 'location_is_visible', 'books', 'posts')

class UserOtherPhoneLocationSerializer(serializers.ModelSerializer):
    posts = PostUserSerializer(many=True, required=False, source='post_user', read_only=True)
    books = BookUserSerializer(many=True, required=False, source='book_user', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture',
                  'region', 'district', 'location', 'books', 'posts')

class UserOtherPhoneSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    posts = PostUserSerializer(many=True, required=False, source='post_user', read_only=True)
    books = BookUserSerializer(many=True, required=False, source='book_user', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture',
                  'region', 'district', 'location', 'books', 'posts')
    def get_location(self, obj):
        return


class UserOtherLocationSerializer(serializers.ModelSerializer):
    posts = PostUserSerializer(many=True, required=False, source='post_user', read_only=True)
    books = BookUserSerializer(many=True, required=False, source='book_user', read_only=True)
    phone_number = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture',
                  'region', 'district', 'location', 'books', 'posts')
    def get_phone_number(self, obj):
        return

class UserOtherSerializer(serializers.ModelSerializer):
    posts = PostUserSerializer(many=True, required=False, source='post_user', read_only=True)
    books = BookUserSerializer(many=True, required=False, source='book_user', read_only=True)
    phone_number = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'picture', 'region',
                  'district', 'location', 'books', 'posts')
    def get_phone_number(self, obj):
        return
    def get_location(self, obj):
        return


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number')
