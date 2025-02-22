from django.urls import path
from .views import PostViewSet, PostCommentViewSet

urlpatterns = [
    path('<int:pk>/', PostViewSet.as_view(
        {'get': 'post_detail', 'delete': 'post_delete', 'patch': 'post_update', 'post': 'post_like'})),
    path('', PostViewSet.as_view(
        {'get': 'post_list', 'post': 'post_create'})),
    path('<int:pk>/comment/', PostCommentViewSet.as_view(
        {'post': 'post_comment_create'})),
    path('comment/<int:pk>/', PostCommentViewSet.as_view(
        {'delete': 'post_comment_delete', 'post': 'post_comment_like'})),
]