# members/urls.py
from django.urls import path
from . import views

app_name = 'members'  # Esto registra el namespace 'members'

urlpatterns = [
    path('especialistas/', views.especialistas_view, name='especialistas_view'),
]
