from users.api_endpoints import *
from django.urls import path

urlpatterns = [
    path('bot/register/', UserViewSet.as_view({'post': 'bot_user_register'}), name='bot_register'),
    path('bot/language/', GetBotLanguageViewSet.as_view({'get': 'get_language'}), name='bot_user_language'),
    path('bot/update/', BotUserUpdateViewSet.as_view({'patch': 'update_bot_user'}), name='update_bot_user_data'),
    path('bot/generate_otp/', SendOtpViewSet.as_view({'post': 'generate_otp_code'}), name='generate_otp_code'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='refresh-token'),
    path('me/', UserProfileAPIView.as_view(), name='user-profile'),
    path('<int:pk>/', OtherUserDetailAPIView.as_view(), name='other-user-detail'),
    path('me/update/', UserUpdateAPIView.as_view(), name='user-update'),
]
