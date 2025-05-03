from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm

def home(request):
    if request.user.is_authenticated:
        # Redirect based on role
        if request.user.is_teacher():
            return redirect('prof:dashboard')
        else:
            return redirect('student:exam_list')
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
