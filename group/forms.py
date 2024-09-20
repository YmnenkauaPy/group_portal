from django import forms
from group import models
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

class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)

    class Meta:
        model = models.CustomUser
        fields = ['username', 'details', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(),
        }