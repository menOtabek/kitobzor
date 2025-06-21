from django.urls import path, include

urlpatterns = [
    path('', include('shop.api_endpoints.Shop.urls')),
    # path('stuff/', include('shop.api_endpoints.ShopAdmin.urls')),
]
