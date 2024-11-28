# my_tennis_club/urls.py (archivo principal de URLs)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),  # Incluye las URLs de la aplicación 'members'
]
