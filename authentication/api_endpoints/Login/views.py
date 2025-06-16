from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from authentication.models import User
from authentication.api_endpoints.Login.serializers import LoginSerializer, TokenSerializer


class LoginAPIViewSet(ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Login",
        request_body=LoginSerializer,
        responses={200: TokenSerializer()},
        tags=['User']
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)

        user = User.objects.filter(otp_user__otp_code=serializer.validated_data.get('otp_code')).first()

        if not user:
            raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Code is invalid')

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['role'] = user.role

        user.otp_user.delete()
        return Response(data={'result': {'access_token': str(access_token), 'refresh_token': str(refresh_token)},
                              'success': True}, status=status.HTTP_200_OK)


__all__ = ['LoginAPIViewSet']
