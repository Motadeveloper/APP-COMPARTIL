from django.urls import path
from . import views

urlpatterns = [
    
    path('reservar/', views.reservar_data, name='reservar_data'),
    
] 