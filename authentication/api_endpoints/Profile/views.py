from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from authentication.models import User
from authentication.api_endpoints.Profile.serializers import ProfileSerializer


class ProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="User detail",
        description="Detail of the user",
        responses={200: ProfileSerializer},
        tags=['User']
    )
    def user_detail(self, request):
        user = User.objects.filter(id=request.user.id).prefetch_related('book_user').first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')

        serializer = ProfileSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


__all__ = ['ProfileViewSet']
