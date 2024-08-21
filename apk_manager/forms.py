from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import App


# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# App Upload Form
class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ["name", "apk_file_path"]
