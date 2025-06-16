from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from authentication.models import User
from authentication.api_endpoints.RefreshToken.serializers import RefreshTokenSerializer
from authentication.api_endpoints.Login.serializers import TokenSerializer


class RefreshTokenViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Refresh token",
        operation_description="Refresh token",
        request_body=RefreshTokenSerializer,
        responses={200: TokenSerializer()},
        tags=['User']
    )
    def refresh_token(self, request):
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
        new_access_token['role'] = user.role

        return Response(
            data={'result': {'access_token': str(new_access_token), 'refresh_token': str(new_refresh_token)},
                  'success': True}, status=status.HTTP_200_OK)


__all__ = ['RefreshTokenViewSet']
