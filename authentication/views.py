from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .serializers import UserCreateSerializer, UserUpdateSerializer, OtpGenerateSerializer, LoginSerializer
from .models import User
from .utils import otp_generate

class UserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='User create with bot data',
        operation_description='User create with bot data',
        request_body=UserCreateSerializer,
        responses={201: UserCreateSerializer()},
        tags=['User']
    )
    def register(self, request):
        telegram_id = request.data.get('telegram_id')
        if User.objects.filter(telegram_id=telegram_id).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="User's data update",
        operation_description="User's data update",
        request_body=UserUpdateSerializer,
        responses={200: UserUpdateSerializer()},
        tags=['User']
    )
    def update_user_data(self, request):
        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message="User not found")
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Otp code generate",
        operation_description="Otp code generate for user",
        request_body=OtpGenerateSerializer,
        responses={201: OtpGenerateSerializer()},
        tags=['User']
    )
    def generate_otp_code(self, request):
        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')
        otp_code = otp_generate(user)
        user.otp_code = otp_code
        user.save(update_fields=['otp_code'])
        return Response(data={'otp_code': otp_code, 'success': True}, status=status.HTTP_201_CREATED)
