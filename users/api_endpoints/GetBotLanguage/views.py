from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from users.models import User
from users.api_endpoints.GetBotLanguage.serializers import GetLanguageSerializer
from users.utils import IsMyBot


class GetBotLanguageViewSet(ViewSet):
    permission_classes = [IsMyBot]

    @extend_schema(
        summary="Get bot language",
        tags=['Bot']
    )
    def get_language(self, request):

        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()

        if not user:
            return Response(data={'result': '', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        serializer = GetLanguageSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


__all__ = ['GetBotLanguageViewSet']
