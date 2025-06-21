from django.urls import path, include

urlpatterns = [
    path('', include('sharing.api_endpoints.Book.urls')),
    path('comment/', include('sharing.api_endpoints.BookComment.urls')),
]
