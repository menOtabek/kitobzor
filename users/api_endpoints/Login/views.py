from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from users.models import User
from users.api_endpoints.Login.serializers import LoginSerializer, TokenSerializer


class LoginAPIViewSet(ViewSet):
    permission_classes = [AllowAny]
    print('shotta')
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: TokenSerializer,
            400: OpenApiResponse(description="Invalid input"),
        },
        tags=["User"],
        summary="Login",
        description="Login with OTP code and receive JWT tokens"
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
        print('shotta 2')
        user = User.objects.filter(otp_user__otp_code=serializer.validated_data.get('otp_code'),
                                   phone_number=serializer.validated_data.get('phone_number')).first()

        if not user:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Code or phone number is invalid')

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['role'] = user.role

        user.otp_user.delete()
        return Response(data={'result': {'access_token': str(access_token), 'refresh_token': str(refresh_token)},
                              'success': True}, status=status.HTTP_200_OK)


__all__ = ['LoginAPIViewSet']
