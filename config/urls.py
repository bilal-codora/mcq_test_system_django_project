from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
