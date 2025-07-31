from django.urls import path
from .views import (
    RegionViewSet, DistrictViewSet,
    BannerViewSet, FAQViewSet, PrivacyPolicyViewSet, ContactUsCreateAPIView
)

urlpatterns = [
    path('regions/', RegionViewSet.as_view({'get': 'list'}), name='region-list'),
    path('districts/', DistrictViewSet.as_view({'get': 'list'}), name='district-list'),
    path('banners/', BannerViewSet.as_view({'get': 'list'}), name='banner-list'),
    path('faqs/', FAQViewSet.as_view({'get': 'list'}), name='faq-list'),
    path('policies/', PrivacyPolicyViewSet.as_view({'get': 'list'}), name='policy-list'),
    path('contact-us/', ContactUsCreateAPIView.as_view(), name='contact-us-create'),
]
