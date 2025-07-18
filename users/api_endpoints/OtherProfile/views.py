from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from users.models import User
from users.api_endpoints.OtherProfile.serializers import UserOtherSerializer

@extend_schema(tags=['User'],
               responses={200: UserOtherSerializer},
               summary='Get User Other Profile',)
class OtherUserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserOtherSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


__all__ = ['OtherUserDetailAPIView']