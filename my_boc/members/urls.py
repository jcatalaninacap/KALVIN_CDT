from django.urls import path,include
from . import views

urlpatterns = [
    path('', include('members.urls')),
    path('members/', views.members, name='members'),
]