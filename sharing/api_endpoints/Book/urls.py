from django.urls import path
from sharing.api_endpoints.Book.views import BookViewSet, BookLikeViewSet, CategoryViewSet

urlpatterns = [
    path('create/', BookViewSet.as_view({'post': 'create'})),
    path('list/', BookViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', BookViewSet.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'})),
    path('liked/', BookViewSet.as_view({'get': 'liked'})),
    path('like/', BookLikeViewSet.as_view({'post': 'create'})),
    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
]
