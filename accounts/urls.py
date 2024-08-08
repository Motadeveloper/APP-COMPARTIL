from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [ 
    path('', views.register, name='register'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout')
] 