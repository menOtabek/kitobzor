from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_spectacular.utils import extend_schema

from users.api_endpoints.RefreshToken.serializers import RefreshTokenSerializer
from users.api_endpoints.Login.serializers import TokenSerializer
from users.models import User


class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RefreshTokenSerializer,
        responses={200: TokenSerializer},
        summary="Refresh token",
        description="Refresh access and refresh token using refresh token",
        tags=["User"]
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            old_refresh = RefreshToken(serializer.validated_data['refresh_token'])
        except TokenError as e:
            raise ValidationError(f'Invalid token: {str(e)}')

        user_id = old_refresh.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise ValidationError('User not found')

        try:
            old_refresh.blacklist()
        except Exception:
            pass

        new_refresh = RefreshToken.for_user(user)
        new_access = new_refresh.access_token
        new_access['role'] = user.role

        return Response({
            "access_token": str(new_access),
            "refresh_token": str(new_refresh)
        }, status=status.HTTP_200_OK)


__all__ = ['RefreshTokenAPIView']