from drf_spectacular.utils import extend_schema
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from users.api_endpoints.UpdateUser.serializers import UserUpdateSerializer


@extend_schema(summary="User update",
               description="Update authenticated user information",
               tags=['User'])
class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


__all__ = ["UserUpdateAPIView"]
