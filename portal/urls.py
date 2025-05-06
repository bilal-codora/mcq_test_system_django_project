from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from portal.views import RoleBasedLoginView, custom_logout
from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]
