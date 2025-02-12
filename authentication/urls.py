from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'})),
    path('update/', UserViewSet.as_view({'patch': 'update_user_data'})),
    path('generate_otp/', UserViewSet.as_view({'post': 'generate_otp_code'})),
]