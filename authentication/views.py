from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .models import User
from .utils import otp_generate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserCreateSerializer, BotUserUpdateSerializer, LoginSerializer,
    TokenSerializer, RefreshTokenSerializer, UserUpdateSerializer,
    UserSerializer, UserOtherSerializer, UserOtherPhoneSerializer,
    UserOtherLocationSerializer, UserOtherPhoneLocationSerializer,
    UserMeSerializer, GetLanguageSerializer)


class UserViewSet(ViewSet):
    def bot_user_register(self, request):
        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if user:
            return Response(status=status.HTTP_409_CONFLICT)
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        language_serializer = GetLanguageSerializer(user, context={'request': request})
        return Response(data={'result': language_serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    def get_language(self, request):
        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GetLanguageSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    def update_bot_user_data(self, request):
        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BotUserUpdateSerializer(instance=user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        serializer = GetLanguageSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    def generate_otp_code(self, request):
        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if not user:
            return Response(data={'success': False}, status=status.HTTP_404_NOT_FOUND)
        response = otp_generate(user)
        return Response(data={'result': response, 'success': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Login",
        request_body=LoginSerializer,
        responses={200: TokenSerializer()},
        tags=['User']
    )
    def login(self, request):
        login_time = timezone.now().isoformat()
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
        user = User.objects.filter(otp_code=request.data.get('otp_code'),
                                   phone_number=request.data.get('phone_number')).first()
        if not user:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Phone number or code is invalid')
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['login_time'] = login_time
        user.login_time = login_time
        user.save(update_fields=['login_time'])
        user.otp_code.delete()
        return Response(data={'result': {'access_token': str(access_token), 'refresh_token': str(refresh_token)},
                              'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Refresh token",
        operation_description="Refresh token",
        request_body=RefreshTokenSerializer,
        responses={200: TokenSerializer()},
        tags=['User']
    )
    def refresh_token(self, request):
        login_time = timezone.now().isoformat()
        serializer = RefreshTokenSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
        refresh = RefreshToken(serializer.validated_data.get('refresh_token'))
        user_id = refresh.payload.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='User not found')
        new_refresh_token = RefreshToken.for_user(user)
        new_access_token = new_refresh_token.access_token
        new_access_token['login_time'] = login_time
        new_access_token['role'] = user.role
        user.login_time = login_time
        user.save(update_fields=['login_time'])
        return Response(
            data={'result': {'access_token': str(new_access_token), 'refresh_token': str(new_refresh_token)},
                  'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="User update",
        operation_description="User update",
        request_body=UserUpdateSerializer,
        responses={200: UserUpdateSerializer()},
        tags=['User']
    )
    def user_update(self, request):
        user = request.user
        if not user:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='User not found')
        serializer = UserUpdateSerializer(instance=user, data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Other user detail",
        operation_description="Detail of other user",
        responses={200: UserOtherPhoneLocationSerializer()},
        tags=['User']
    )
    def other_user_detail(self, request, pk=None):
        user = User.objects.filter(id=pk).prefetch_related('post_user', 'book_user').first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')
        if user.phone_is_visible is True and user.location_is_visible is True:
            serializer = UserOtherPhoneLocationSerializer(user, context={'request': request})
        elif user.phone_is_visible is True and user.location_is_visible is False:
            serializer = UserOtherPhoneSerializer(user, context={'request': request})
        elif user.phone_is_visible is False and user.location_is_visible is True:
            serializer = UserOtherLocationSerializer(user, context={'request': request})
        else:
            serializer = UserOtherSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="User detail",
        operation_description="Detail of the user",
        responses={200: UserSerializer()},
        tags=['User']
    )
    def user_detail(self, request):
        user = User.objects.filter(id=request.user.id).prefetch_related('post_user', 'book_user').first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')
        serializer = UserSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Check auth me",
        operation_description="Check authentication of user",
        responses={200: UserMeSerializer()},
        tags=['User']
    )
    def check_auth(self, request):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')
        serializer = UserMeSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)
