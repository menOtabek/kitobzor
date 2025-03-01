from django.urls import path
from .views import RegionViewSet, DistrictViewSet, BannerViewSet, FAQViewSet, PrivacyPolicyViewSet

urlpatterns = [
    path('region/', RegionViewSet.as_view({'get': 'get_region'}), name='region'),
    path('region/<int:pk>/', DistrictViewSet.as_view({'get': 'get_district'}), name='district'),
    path('banners/', BannerViewSet.as_view({'get': 'get_banners'}), name='banners'),
    path('faq/', FAQViewSet.as_view({'get': 'get_faq_list'}), name='faq_list'),
    path('faq/<int:pk>/', FAQViewSet.as_view({'get': 'get_faq_detail'}), name='faq_detail'),
    path('policy/', PrivacyPolicyViewSet.as_view({'get': 'get_privacy_policies'}), name='policies'),
    path('policy/<int:pk>/', PrivacyPolicyViewSet.as_view({'get': 'get_privacy_policy_detail'}), name='policy'),
]
