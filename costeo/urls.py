# costeo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('registrar_empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('registrar_costeo/', views.registrar_costeo, name='registrar_costeo'),
    path('costo_mano_obra/', views.manoDeObra, name='costo_mano_obra'),
]
