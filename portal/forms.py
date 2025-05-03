from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from django.contrib.auth import get_user_model
User = get_user_model()  # This will be portal.User
# Then use User (portal.User) when creating users or querying.


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

# # portal/forms.py
# from django.contrib.auth.forms import UserCreationForm
# from portal.models import User

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         # include the role field so it appears on the signup form:
#         fields = UserCreationForm.Meta.fields + ('role',)
