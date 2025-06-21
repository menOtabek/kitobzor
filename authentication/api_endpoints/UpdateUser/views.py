from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from authentication.api_endpoints.UpdateUser.serializers import UserUpdateSerializer


class UpdateUserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="User update",
        description="Update authenticated user information",
        request=UserUpdateSerializer,
        responses={200: UserUpdateSerializer},
        tags=['User']
    )
    def user_update(self, request):
        user = request.user
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.INVALID_INPUT, serializer.errors)
        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


__all__ = ['UpdateUserViewSet']
