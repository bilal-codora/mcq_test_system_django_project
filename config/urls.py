from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),      # Home, login, register
    path('teacher/', include('prof.urls')),   # Teacher (prof) URLs
    path('student/', include('student.urls')), # Student URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
