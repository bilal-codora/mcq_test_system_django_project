from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm


from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import redirect

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('portal:home')



class RoleBasedLoginView(LoginView):
    template_name = 'portal/login.html'
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_teacher():
                return reverse('teacher:dashboard') 
            elif user.is_student():
                return reverse('student:exam_list') 
        return reverse('portal:home')




def home(request):
   
    return render(request, 'portal/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set password and role
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'portal/register.html', {'form': form})
