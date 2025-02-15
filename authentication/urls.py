from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('bot/register/', UserViewSet.as_view({'post': 'bot_user_register'})),
    path('bot/update/', UserViewSet.as_view({'patch': 'update_bot_user_data'})),
    path('bot/generate_otp/', UserViewSet.as_view({'post': 'generate_otp_code'})),
    path('login/', UserViewSet.as_view({'post': 'login'})),
    path('refresh/', UserViewSet.as_view({'post': 'refresh_token'})),
    path('update/', UserViewSet.as_view({'patch': 'user_update'})),
]