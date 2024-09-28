from django import forms
from authentication import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['details', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(),
        }

