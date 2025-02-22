from django.urls import path
from .views import BookViewSet, BookCommentViewSet

urlpatterns = [
    path('<int:pk>/', BookViewSet.as_view(
        {'get': 'get_a_book', 'patch': 'update_a_book', 'delete': 'delete_a_book', 'post': 'like_a_book'})),
    path('', BookViewSet.as_view(
        {'get': 'books_list', 'post': 'create_a_book'})),
    path('<int:pk>/comment/', BookCommentViewSet.as_view(
        {'post': 'create_a_book_comment'})),
    path('comment/<int:pk>/',BookCommentViewSet.as_view(
        {'post': 'like_a_book_comment', 'delete': 'delete_a_book_comment'})),
]
