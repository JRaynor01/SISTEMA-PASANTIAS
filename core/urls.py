from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('pasantia/', include('pasantia.urls', namespace="pasantia")),
    path('users/', include('accounts.urls', namespace="users")),
    path('', HomeView, name='home'),
    path('informacion/<post>/', viewInformation, name="info"),
    path('finalizados/post', postfinalizados, name="postfinalizados"),
    path('buscador/',buscador, name="buscador")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)