from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from users.models import User
from users.api_endpoints.OtherProfile.serializers import UserOtherSerializer


class OtherProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Other user detail",
        description="Detail of another user by ID",
        responses={
            200: UserOtherSerializer,
            404: OpenApiResponse(description="User not found")
        },
        tags=["User"],
    )
    def other_user_detail(self, request, pk=None):
        user = User.objects.filter(id=pk, is_active=True).prefetch_related('book_user').first()

        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')

        serializer = UserOtherSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


__all__ = ['OtherProfileViewSet']
