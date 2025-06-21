from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from authentication.models import User
from authentication.utils import otp_generate, IsMyBot


class SendOtpViewSet(ViewSet):
    permission_classes = [IsMyBot]

    @extend_schema(
        summary="Send OTP",
        tags=['Bot']
    )
    def generate_otp_code(self, request):

        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()

        if not user:
            return Response(data={'success': False}, status=status.HTTP_404_NOT_FOUND)

        response = otp_generate(user)
        return Response(data={'result': response, 'success': True}, status=status.HTTP_201_CREATED)


__all__ = ['SendOtpViewSet']
