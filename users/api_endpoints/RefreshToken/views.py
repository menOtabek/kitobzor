from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.api_endpoints.Login.serializers import TokenSerializer
from users.api_endpoints.RefreshToken.serializers import RefreshTokenSerializer
from users.models import User
from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException


class RefreshTokenViewSet(ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Refresh token",
        description="Refresh access and refresh token using existing refresh token",
        request=RefreshTokenSerializer,
        responses={200: TokenSerializer},
        tags=['User']
    )
    def refresh_token(self, request):
        serializer = RefreshTokenSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)

        try:
            refresh = RefreshToken(serializer.validated_data.get('refresh_token'))
        except TokenError as e:
            raise CustomApiException(ErrorCodes.UNAUTHORIZED, message='Token is blacklisted')

        user_id = refresh.payload.get('user_id')
        user = User.objects.filter(id=user_id).first()

        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')

        new_refresh_token = RefreshToken.for_user(user)
        new_access_token = new_refresh_token.access_token
        new_access_token['role'] = user.role

        return Response(
            data={'result': {'access_token': str(new_access_token), 'refresh_token': str(new_refresh_token)},
                  'success': True}, status=status.HTTP_200_OK)


__all__ = ['RefreshTokenViewSet']
