from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Form for user registration
class RegisterForm(forms.Form):
    # Username field with a text input widget and Bootstrap styling
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Email field with an email input widget and Bootstrap styling
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # Password field with a password input widget to hide text
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Custom validation to check if the username already exists
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")  # Raise an error if the username exists
        return username  # Return valid username

    # Custom validation to check if the email is already registered
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")  # Raise an error if email exists
        return email  # Return valid email

    # Save method to create a new user
    def save(self, commit=True):
        # Create a new user with the provided username, email, and password
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user  # Return the created user instance


# Form for user login
class LoginForm(forms.Form):
    # Username field with a text input widget
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Password field with a password input widget
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Custom validation to authenticate user
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Authenticate the user using Django's built-in authentication system
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password.")  # Raise an error if authentication fails
        
        cleaned_data['user'] = user  # Store the authenticated user in cleaned_data
        return cleaned_data  # Return the cleaned data


# Form for updating user profile (username & email)
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Link the form to Django's built-in User model
        fields = ['username', 'email']  # Fields that can be updated
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),  # Add Bootstrap styling
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    # Override the form initialization method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True  # Ensure username is required
        self.fields['email'].required = True  # Ensure email is required


# Form for changing user password
class ChangePasswordForm(forms.Form):
    # Old password field for verification
    old_password = forms.CharField(label="Old Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # New password field
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # Confirmation field to ensure the user entered the new password correctly
    confirm_new_password = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Custom initialization to store the current user
    def __init__(self, user, *args, **kwargs):
        self.user = user  # Store the user instance
        super().__init__(*args, **kwargs)

    # Validate the old password
    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        # Check if the entered old password matches the user's current password
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")  # Raise an error if incorrect
        return old_password  # Return valid old password

    # Validate new password and confirmation
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        # Ensure the new password and confirmation match
        if new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match.")  # Raise an error if they don't match

        return cleaned_data  # Return validated data

    # Save the new password
    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])  # Set the new password
        self.user.save()  # Save the user instance with the new password
        return self.user  # Return the updated user instance
