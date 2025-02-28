from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('bot/register/', UserViewSet.as_view({'post': 'bot_user_register'}), name='bot_register'),
    path('bot/update/', UserViewSet.as_view({'patch': 'update_bot_user_data'}), name='update_bot_user_data'),
    path('bot/generate_otp/', UserViewSet.as_view({'post': 'generate_otp_code'}), name='generate_otp_code'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('refresh/', UserViewSet.as_view({'post': 'refresh_token'}), name='refresh_token'),
    path('me/', UserViewSet.as_view({'get': 'user_detail', 'patch': 'user_update'}), name='user_detail'),
    path('<int:pk>/', UserViewSet.as_view({'get': 'other_user_detail'}), name='other_user_detail'),
    path('me/check/', UserViewSet.as_view({'get': 'check_auth'}), name='check_auth'),
]