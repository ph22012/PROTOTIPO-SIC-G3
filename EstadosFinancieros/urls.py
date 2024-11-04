from django.urls import path
from . import views

urlpatterns = [
    path('gestionar/', views.gestionar),
    path('gestionar/balance-comprobacion/', views.comprobacion),
    
]