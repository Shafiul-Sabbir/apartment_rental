from django.shortcuts import render, redirect  # Import functions to render templates and redirect users
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout  # Import authentication functions
from django.contrib import messages  # Import messages framework for displaying success/error messages
from .forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm  # Import custom forms

# User Registration

def register(request):
    """Handles user registration."""
    if request.method == 'POST':  # Check if the request is a POST request (form submission)
        form = RegisterForm(request.POST)  # Initialize the registration form with submitted data
        if form.is_valid():  # Validate the form data
            form.save()  # Save the new user to the database
            form = RegisterForm()  # Reset the form after successful registration
            messages.success(request, "User created successfully. You can now log in.")  # Display success message
            return redirect('login')  # Redirect to login page
        else:
            error = form.errors  # Capture form errors
            return render(request, 'authentication/register.html', {'form': form, 'error': error})  # Re-render form with errors
    else:
        form = RegisterForm()  # If GET request, initialize an empty form
    
    return render(request, 'authentication/register.html', {'form': form})  # Render the registration page


# User Login
def login(request):
    """Handles user login."""
    if request.method == 'POST':  # Check if the request is a POST request (form submission)
        form = LoginForm(request.POST)  # Initialize the login form with submitted data
        if form.is_valid():  # Validate the form data
            user = form.cleaned_data['user']  # Get authenticated user from cleaned data
            auth_login(request, user)  # Log the user in
            form = LoginForm()  # Reset the form after successful login
            messages.success(request, "Login successful.")  # Display success message
            return redirect('tenant_list')  # Redirect to the tenant list page (dashboard)
        else:
            error = form.errors  # Capture form errors
            return render(request, 'authentication/login.html', {'form': form, 'error': error})  # Re-render form with errors
    else:
        form = LoginForm()  # If GET request, initialize an empty login form
    
    return render(request, 'authentication/login.html', {'form': form})  # Render the login page


# User Logout
def logout(request):
    """Handles user logout."""
    auth_logout(request)  # Log the user out
    messages.success(request, "Logout successful.")  # Display success message
    return redirect('login')  # Redirect to login page

# Update Profile
def update_profile(request):
    """Handles user profile updates."""
    if request.method == 'POST':  # Check if the request is a POST request (form submission)
        form = UpdateProfileForm(request.POST, instance=request.user)  # Initialize form with current user instance
        if form.is_valid():  # Validate the form data
            form.save()  # Save updated profile data
            messages.success(request, 'Your profile was successfully updated!')  # Display success message
            return redirect('tenant_list')  # Redirect to tenant list page
        else:
            error = form.errors  # Capture form errors
            return render(request, 'authentication/update_profile.html', {'form': form, 'error': error})  # Re-render form with errors
    else:
        form = UpdateProfileForm(instance=request.user)  # If GET request, pre-fill form with current user data
    
    return render(request, 'authentication/update_profile.html', {'form': form})  # Render the profile update page


# Change Password
def change_password(request):
    """Handles password changes for logged-in users."""
    if request.method == 'POST':  # Check if the request is a POST request (form submission)
        form = ChangePasswordForm(user=request.user, data=request.POST)  # Initialize form with user instance and submitted data
        if form.is_valid():  # Validate the form data
            form.save()  # Save the new password
            messages.success(request, 'Your password was successfully updated!')  # Display success message
            return redirect('tenant_list')  # Redirect to tenant list page
        else:
            error = form.errors  # Capture form errors
            return render(request, 'authentication/change_password.html', {'form': form, 'error': error})  # Re-render form with errors
    else:
        form = ChangePasswordForm(user=request.user)  # If GET request, initialize an empty password change form
    
    return render(request, 'authentication/change_password.html', {'form': form})  # Render the password change page