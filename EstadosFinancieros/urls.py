from django.urls import path
from . import views
urlpatterns = [
    path('gestion/', views.gestionar),
]