from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    # Add any custom fields if necessary, otherwise just use the standard ones
    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'})
    )
