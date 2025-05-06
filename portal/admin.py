from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from portal.models import User


class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'role', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login',
    )

admin.site.register(User, UserAdmin)