from django.urls import path
from .views import RegionViewSet, DistrictViewSet, DefaultBookOfferViewSet

urlpatterns = [
    path('region/', RegionViewSet.as_view({'get': 'get_region'}), name='region'),
    path('region/<int:pk>/', DistrictViewSet.as_view({'get': 'get_district'}), name='district'),
    path('offer/', DefaultBookOfferViewSet.as_view({'get': 'get_offer', 'post': 'create_offer'}), name='book_offer'),
]