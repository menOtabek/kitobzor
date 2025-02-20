from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import District, Region, Banner
from .serializers import (DistrictSerializer, RegionSerializer, BannerSerializer)


class RegionViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Region list',
        operation_description='List all regions',
        responses={status.HTTP_200_OK: DistrictSerializer(many=True)},
        tags=['Region']
    )
    def get_region(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


class DistrictViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='District list',
        operation_description='List of Districts by Region ID',
        responses={status.HTTP_200_OK: DistrictSerializer(many=True)},
        tags=['District']
    )
    def get_district(self, request, pk):
        districts = District.objects.get(region_id=pk)
        serializer = DistrictSerializer(districts, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


class BannerViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Banner list',
        operation_description='List of banners',
        responses={200: BannerSerializer(many=True)},
        tags=['Banner']
    )
    def get_banners(self, request):
        banners = Banner.objects.filter(is_active=True).order_by('-created_at')[:7]
        serializer = BannerSerializer(banners, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)
