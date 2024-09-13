"""
URL configuration for plated project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('subject/', include('subjects.urls')),
    path('user/', include('users.urls')),
    path('auth/', include('auth.urls')),
    path('exam/', include('exams.urls')),
    path('dashboard/', include('dashboard.urls')),
    path(r'^_nested_admin/', include('nested_admin.urls')),
    path('', include('home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
