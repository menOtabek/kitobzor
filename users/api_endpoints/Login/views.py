from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.api_endpoints.Login.serializers import LoginSerializer, TokenSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

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
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(
                otp_user__otp_code=serializer.validated_data['otp_code'],
                phone_number=serializer.validated_data['phone_number'],
                is_active=True
            )
        except User.DoesNotExist:
            raise ValidationError("Code or phone number is invalid")

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access['role'] = user.role

        user.otp_user.delete()

        return Response({
            "access_token": str(access),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)


__all__ = ['LoginAPIView']
