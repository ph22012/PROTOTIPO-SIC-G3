from django.urls import path
from . import views

urlpatterns = [
    path('gestionar/', views.gestionar),
    path('gestionar/balance-comprobacion/', views.comprobacion),
    path('gestionar/estado-resultado/', views.resultados),
    path('gestionar/balance-general/', views.general),
    path('gestionar/ajustes/', views.ajustes),
    path('gestionar/balance_ajustado/', views.comprobacionAjustado, name='balance_Ajustado'),
    path('gestionar/estado_capital/', views.capital),
    
]