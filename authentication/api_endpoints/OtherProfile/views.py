from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from authentication.models import User
from authentication.api_endpoints.OtherProfile.serializers import UserOtherSerializer


class OtherProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Other user detail",
        operation_description="Detail of other user",
        responses={200: UserOtherSerializer()},
        tags=['User']
    )
    def other_user_detail(self, request, pk=None):
        user = User.objects.filter(id=pk, is_banned=False, is_active=True).prefetch_related('book_user').first()

        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')

        serializer = UserOtherSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


__all__ = ['OtherProfileViewSet']
