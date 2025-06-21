from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


admin.site.site_header = 'Kitobzor Admin'
admin.site.site_title = 'Kitobzor Admin'
admin.site.index_title = 'Welcome to dashboard'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/base/', include('base.urls')),
    path('api/v1/book/', include('sharing.urls')),
    # path('api/v1/post/', include('blog.urls')),
    path('api/v1/shop/', include('shop.urls')),
]


if settings.SHOW_SWAGGER:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
