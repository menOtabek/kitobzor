from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop.models import ShopStuff, Shop
from shop.api_endpoints.ShopAdmin.serializers import ShopStuffSerializer
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


class ShopStuffViewSet(ModelViewSet):
    queryset = ShopStuff.objects.select_related('shop', 'user').all()
    serializer_class = ShopStuffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShopStuff.objects.filter(shop__owner=self.request.user)

    def perform_create(self, serializer):
        shop = serializer.validated_data.get('shop')
        if shop.owner != self.request.user:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You do not own this shop.")
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        self.perform_create(serializer)
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.shop.owner != request.user:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You can only update admins of your own shop.")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.shop.owner != request.user:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message="You can only delete admins of your own shop.")
        instance.is_banned = True
        instance.save(update_fields=['is_banned'])
        return Response(data={'result': 'Admin removed', 'success': True}, status=status.HTTP_204_NO_CONTENT)
