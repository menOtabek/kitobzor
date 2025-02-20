from django.urls import path
from .views import RegionViewSet, DistrictViewSet, BannerViewSet

urlpatterns = [
    path('region/', RegionViewSet.as_view({'get': 'get_region'}), name='region'),
    path('region/<int:pk>/', DistrictViewSet.as_view({'get': 'get_district'}), name='district'),
    path('banners/', BannerViewSet.as_view({'get': 'get_banners'}), name='banners'),
]
