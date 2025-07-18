from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.filters import OrderingFilter
from utils.filters import ShopFilter

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from shop.api_endpoints.Shop.serializers import (
    ShopUpdateSerializer,
    ShopDetailSerializer,
    ShopListSerializer
)
from shop.models import Shop


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (OrderingFilter, ShopFilter)

    @extend_schema(
        summary="Update shop",
        request=ShopUpdateSerializer,
        responses={200: ShopUpdateSerializer},
        tags=["Shop"]
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_active is False:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message='Shop is not active.')
        if instance.owner != request.user:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message='You are not owner of this shop.')

        serializer = ShopUpdateSerializer(instance, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Shop.objects.filter(is_active=True)

    @extend_schema(
        summary="List shops",
        parameters=ShopFilter.generate_query_parameters(),
        responses={200: ShopListSerializer(many=True)},
        tags=["Shop"]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ShopListSerializer(queryset, many=True, context={'request': request})
        return Response({'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Get shop detail",
        responses={200: ShopDetailSerializer},
        tags=["Shop"])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        can_update = instance.owner == request.user
        if instance.is_active is False:
            raise CustomApiException(ErrorCodes.FORBIDDEN, message='Shop is not active.')
        serializer = ShopDetailSerializer(instance, context={'request': request})
        data = serializer.data
        data['can_update'] = can_update
        return Response({'result': data, 'success': True}, status=status.HTTP_200_OK)
