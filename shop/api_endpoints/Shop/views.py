from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from shop.api_endpoints.Shop.serializers import (
    ShopUpdateSerializer,
    ShopDetailSerializer,
    ShopListSerializer
)
from shop.models import Shop


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.select_related('region', 'district').all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update shop",
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

    @extend_schema(
        summary="List shops",
        parameters=[
            OpenApiParameter(name='region_id', type=OpenApiTypes.INT, required=False, description="Filter by region id"),
            OpenApiParameter(name='district_id', type=OpenApiTypes.INT, required=False, location=OpenApiParameter.QUERY, description="Filter by district id")
        ],
        responses={200: ShopListSerializer(many=True)},
        tags=["Shop"]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_active=True)

        region_id = request.query_params.get('region_id')
        district_id = request.query_params.get('district_id')

        if region_id:
            queryset = queryset.filter(region_id=region_id)
        if district_id:
            queryset = queryset.filter(district_id=district_id)

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
