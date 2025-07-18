from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from drf_spectacular.utils import extend_schema

from users.api_endpoints.Profile.serializers import ProfileSerializer

@extend_schema(tags=['User'])
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="User detail",
        description="Detail of the authenticated user",
        responses={200: ProfileSerializer},
    )
    def get(self, request):
        user = request.user
        if not user or not user.is_authenticated:
            raise NotFound("User not found")

        serializer = ProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


__all__ = ['UserProfileAPIView']
