from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.nurse_register, name='nurse_register'),
    path('dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
]
