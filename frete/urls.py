# frete/urls.py
from django.urls import path
from .views import calcular_entrega

urlpatterns = [
    path('calcular-entrega/', calcular_entrega, name='calcular_entrega'),
]
