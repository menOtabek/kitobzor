from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from utils.response import success_response
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework import status
from .utils import send_telegram_message_code


from .models import Region, District, Banner, FAQ, PrivacyPolicy
from .serializers import (
    RegionSerializer, DistrictSerializer,
    BannerSerializer, FAQSerializer, PrivacyPolicySerializer, ContactUsSerializer
)
from utils.filters import DistrictFilter, PrivacyPolicyFilter


@extend_schema(tags=["Base"])
class RegionViewSet(ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RegionSerializer

    @extend_schema(responses=RegionSerializer(many=True), summary="List of regions")
    def list(self, request, *args, **kwargs):
        return success_response(self.get_serializer(self.get_queryset(), many=True).data)


@extend_schema(tags=["Base"], parameters=DistrictFilter.generate_query_parameters())
class DistrictViewSet(ReadOnlyModelViewSet):
    queryset = District.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DistrictSerializer
    filter_backends = [DistrictFilter, OrderingFilter]

    @extend_schema(responses=DistrictSerializer(many=True), summary="List of districts")
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        return success_response(self.get_serializer(qs, many=True).data)


@extend_schema(tags=["Base"])
class BannerViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banner.objects.filter(is_active=True).order_by('-created_at')

    @extend_schema(responses=BannerSerializer(many=True), summary="List of active banners")
    def list(self, request, *args, **kwargs):
        return success_response(self.get_serializer(self.get_queryset(), many=True).data)


@extend_schema(tags=["Base"])
class FAQViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FAQSerializer

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('-created_at')

    @extend_schema(responses=FAQSerializer(many=True), summary="List of FAQs")
    def list(self, request, *args, **kwargs):
        return success_response(self.get_serializer(self.get_queryset(), many=True).data)


@extend_schema(tags=["Base"], parameters=PrivacyPolicyFilter.generate_query_parameters())
class PrivacyPolicyViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivacyPolicySerializer
    filter_backends = [PrivacyPolicyFilter, OrderingFilter]
    pagination_class = None

    def get_queryset(self):
        return PrivacyPolicy.objects.filter(is_active=True).order_by('-created_at')

    @extend_schema(responses=PrivacyPolicySerializer(many=True), summary="List of privacy policies")
    def list(self, request, *args, **kwargs):
        return success_response(self.get_serializer(self.filter_queryset(self.get_queryset()), many=True).data)


@extend_schema(tags=["Base"])
class ContactUsCreateAPIView(APIView):
    serializer_class = ContactUsSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContactUsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        send_telegram_message_code(instance, request)
        return success_response(serializer.data, code=status.HTTP_201_CREATED)
