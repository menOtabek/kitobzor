from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes
from .models import District, Region, DefaultBookOffer
from .serializers import (
    DistrictSerializer, RegionSerializer,
    DefaultBookOfferCreateSerializer, DefaultBookOfferSerializer)

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
    def get_district(self, request, region_id):
        districts = District.objects.get(region_id=region_id)
        serializer = DistrictSerializer(districts, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)


class DefaultBookOfferViewSet(ViewSet):
    # ToDo authentication must be required
    @swagger_auto_schema(
        operation_summary='Book offer create',
        operation_description='Create book offer',
        request_body=DefaultBookOfferCreateSerializer,
        tags=['BookOffer']
    )
    def create_book_offer(self, request):
        serializer = DefaultBookOfferCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomApiException(ErrorCodes.INVALID_INPUT, message=serializer.errors)
        serializer.save()
        return Response(data={'result': 'Request sent to admins', 'success': True}, status=status.HTTP_201_CREATED)

    # ToDo authentication must be required
    @swagger_auto_schema(
        operation_summary='Book offer list',
        operation_description='List of book offers',
        responses={status.HTTP_200_OK: DistrictSerializer(many=True)},
        tags=['BookOffer']
    )
    def get_book_offer(self, request):
        user = request.user
        book_offers = DefaultBookOffer.objects.filter(user_id=user.id)
        serializer = DefaultBookOfferSerializer(book_offers, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'success': True}, status=status.HTTP_200_OK)
