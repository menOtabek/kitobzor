from django.urls import path
from .views import PostViewSet

urlpatterns = [
    path('<int:pk>', PostViewSet.as_view({'get': 'post_detail', 'delete': 'post_delete', 'patch': 'post_update'})),
    path('', PostViewSet.as_view({'get': 'post_list', 'post': 'post_create'})),
]