from django.urls import path
from shop.api_endpoints.Shop.views import ShopViewSet

urlpatterns = [
    path('list/', ShopViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', ShopViewSet.as_view({'get': 'retrieve', 'patch': 'update'})),
]