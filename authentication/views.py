from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm

# User Registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # clear the register form
            form = RegisterForm()
            messages.success(request, "User created successfully. You can now log in.")
            return redirect('login')
        else:
            error = form.errors
            return render(request, 'authentication/register.html', {'form': form, 'error': error})
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
            # Clear the login form
            form = LoginForm()
            messages.success(request, "Login successful.")
            return redirect('tenant_list')  # Redirect to dashboard
        
        else:
            error = form.errors
            return render(request, 'authentication/login.html', {'form': form, 'error': error})
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


# User Logout
def logout(request):
    auth_logout(request)
    messages.success(request, "Logout successful.")
    return redirect('login')  # Redirect to login page

# Update Profile
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('tenant_list')  # Redirect to tenant list page
        else:
            error = form.errors
            return render(request, 'authentication/update_profile.html', {'form': form, 'error': error})
    else:
        form = UpdateProfileForm(instance=request.user)
    
    return render(request, 'authentication/update_profile.html', {'form': form})


# Change Password
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('tenant_list')  # Redirect to tenant list page
        else:
            error = form.errors
            return render(request, 'authentication/change_password.html', {'form': form, 'error': error})
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'authentication/change_password.html', {'form': form})