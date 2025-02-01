from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm

# User Registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully. You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'authentication/register.html', {'form': form})


# User Login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            messages.success(request, "Login successful.")
            return redirect('tenant_list')  # Redirect to dashboard
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


# User Logout
def logout(request):
    auth_logout(request)
    messages.success(request, "Logout successful.")
    return redirect('login')  # Redirect to login page
