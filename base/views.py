from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from utils.response import success_response

from .models import Region, District, Banner, FAQ, PrivacyPolicy
from .serializers import (
    RegionSerializer, DistrictSerializer,
    BannerSerializer, FAQSerializer, PrivacyPolicySerializer
)


@extend_schema(tags=["Base"])
class RegionViewSet(ModelViewSet):
    queryset = Region.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegionSerializer

    @extend_schema(responses=RegionSerializer(many=True), summary="List of regions")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


@extend_schema(tags=["Base"])
class DistrictViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = DistrictSerializer

    def get_queryset(self):
        region_id = self.kwargs.get('region_id')
        return District.objects.filter(region_id=region_id).order_by('-created_at')

    @extend_schema(responses=DistrictSerializer(many=True), summary="List of districts by region")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


@extend_schema(tags=["Base"])
class BannerViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banner.objects.filter(is_active=True).order_by('-created_at')[:7]

    @extend_schema(responses=BannerSerializer(many=True), summary="List of active banners")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


@extend_schema(tags=["Base"])
class FAQViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('-created_at')

    @extend_schema(responses=FAQSerializer(many=True), summary="List of FAQs")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)


@extend_schema(tags=["Base"])
class PrivacyPolicyViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PrivacyPolicySerializer

    def get_queryset(self):
        return PrivacyPolicy.objects.filter(is_active=True).order_by('-created_at')

    @extend_schema(responses=PrivacyPolicySerializer(many=True), summary="List of privacy policies")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
