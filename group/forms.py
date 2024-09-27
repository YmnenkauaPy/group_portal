from django import forms
from group import models
from group.models import Grade
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

class ForumThreadForm(forms.ModelForm):
    class Meta:
        model = models.ForumThread
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content', 'media']
        widgets = {
            'content': forms.Textarea(),
            "media": forms.FileInput(),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['name', 'description', 'day_month_year', 'time']
        widgets = {
            'day_month_year': forms.DateInput(attrs={'readonly': True,}),
            'time': forms.TimeInput(attrs={'type': 'time'}),         
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = models.Grade
        fields = ['student', 'subject', 'grade']
