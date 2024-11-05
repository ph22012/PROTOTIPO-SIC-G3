from django.urls import path
from . import views

urlpatterns = [
    #path('transaccion/', views.transacciones),
    path('create-transaction/', views.create_transaction, name='create_transaction'),
]