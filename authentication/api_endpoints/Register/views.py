from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from authentication.models import User
from authentication.api_endpoints.Register.serializers import UserCreateSerializer
from authentication.api_endpoints.GetBotLanguage.serializers import GetLanguageSerializer
from authentication.utils import IsMyBot


class UserViewSet(ViewSet):
    permission_classes = [IsMyBot]

    @extend_schema(
        summary="Register new user on bot",
        tags=['Bot']
    )
    def bot_user_register(self, request):

        telegram_id = request.data.get('telegram_id')
        user = User.objects.filter(telegram_id=telegram_id).first()

        if user:
            return Response(data={'result': 'User Already Exists', 'success': False}, status=status.HTTP_409_CONFLICT)
        serializer = UserCreateSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer.save()
        language_serializer = GetLanguageSerializer(user, context={'request': request})
        return Response(data={'result': language_serializer.data, 'success': True}, status=status.HTTP_201_CREATED)


__all__ = ['UserViewSet']
