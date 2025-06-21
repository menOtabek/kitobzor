from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from authentication.models import User
from authentication.api_endpoints.BotUserUpdate.serializers import BotUserUpdateSerializer
from authentication.api_endpoints.GetBotLanguage.serializers import GetLanguageSerializer
from authentication.utils import IsMyBot


class BotUserUpdateViewSet(ViewSet):
    permission_classes = [IsMyBot]

    @extend_schema(
        summary="Update bot user",
        tags=['Bot']
    )
    def update_bot_user(self, request):

        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()

        if not user:
            return Response(data={'result': '', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        serializer = BotUserUpdateSerializer(instance=user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(data={'result': serializer.errors, 'success': False},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        serializer = GetLanguageSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


__all__ = ['BotUserUpdateViewSet']
