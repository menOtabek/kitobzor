from django.urls import path
from sharing.api_endpoints.BookComment.views import BookCommentViewSet, BookLikeViewSet

urlpatterns = [
    path('create/', BookCommentViewSet.as_view({'post': 'create'})),
    path('list/', BookCommentViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', BookCommentViewSet.as_view({'delete': 'destroy'})),
    path('like/', BookLikeViewSet.as_view({'post': 'create'})),
]